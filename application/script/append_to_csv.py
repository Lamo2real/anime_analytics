import pandas as pd
import logging
import boto3
import warnings
from io import StringIO
from botocore.exceptions import ClientError


def csv_logic(df, bucket_name, key_path):
    """join the new dataframe and existing dataframe into one, then update csv"""
    
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=FutureWarning)

        # deduplication section
        try:
            s3_client = boto3.client('s3') #faster performance, (py interpreter checks for the local value first then gloabl)
            

            #### merge existing data with new API fetched data ####
            try:
                s3_object = s3_client.get_object(Bucket=bucket_name, Key=key_path)
                data_from_cloud =s3_object['Body'].read().decode('utf-8')

                if data_from_cloud:
                    df_existing = pd.read_csv(StringIO(data_from_cloud))
                    df_combined = pd.concat([df_existing, df], ignore_index=True) # ignore incremental id, 'concat' kinda acts like a SQL join in a way
                    df_combined.drop_duplicates(subset=['anime_id', 'title'], inplace=True, keep='last') # inplace indicates that it modifies the existing dataframe and doesnt create a new one
                else:
                    df_combined = df
                    logging.info(f'empty file found on {key_path}, overwriting with new data')

            except ClientError as ce:
                if ce.response['Error']['Code'] == 'NoSuchKey':
                    logging.info(f'no file exists on {key_path}')
                    df_combined = df
                else:
                    raise ce
            except Exception as e:
                logging.error(f'something else went wrong in s3: {e}')


            try:
                if 'df_combined' in locals() and not df_combined.empty:
                    # making sure the csv is updated based on new data (deduplicated)
                    csv_buffer = StringIO() #save data in-memeory (lambda usually is set to 512mb RAM)
                    df_combined.to_csv(csv_buffer, index=False)
                    s3_client.put_object(
                        Bucket=bucket_name,
                        Key=key_path,
                        Body=csv_buffer.getvalue()
                    )
                    return
                
                else:
                    logging.warning("df_combined does not exist or is empty. Skipping upload.")
                    return 
            
            except Exception as write_error:
                logging.error(f'failed to write to S3: {write_error}')
                raise write_error

        except Exception as e:
            logging.error(f'error message: {e}')
            return


