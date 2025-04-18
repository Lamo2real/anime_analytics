import pandas as pd
import logging
import warnings
import boto3
from io import StringIO
from botocore.exceptions import ClientError

S3 = boto3.client('s3')

def csv_logic(df, bucket_name, key_path):
    """join the new dataframe and existing dataframe into one, then update csv"""
    
    # deduplication section
    try:
        s3_client = S3 #faster performance, (py interpreter checks for the local value first then gloabl)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=FutureWarning)

            try:
                s3_object = s3_client.get_object(Bucket=bucket_name, Key=key_path)
                data_from_cloud =s3_object['Body'].read().decode('utf-8')
                df_existing = pd.read_csv(StringIO(data_from_cloud))
                
                df_combined = pd.concat([df_existing, df], ignore_index=True) # ignore incremental id, 'concat' kinda acts like a SQL join in a way
                
                df_combined.drop_duplicates(subset=['anime_id', 'title'], inplace=True) # inplace indicates that it modifies the existing dataframe and doesnt create a new one

                column_integers = [ 'episodes', 'duration', 'genre_id_1', 'genre_id_2', 'genre_id_3' ]
                for col in column_integers:
                    if col in df_combined.columns:
                        try:
                            df_combined[col] = df_combined[col].astype(float).round().astype("Int64")
                        except (ValueError,TypeError):
                            logging.warning(f'Could not convert {col} to Int64. Keeping original dtype.')
                            continue
                        

                

            except ClientError as ce:
                if ce.response['Error']['Code'] == 'NoSuchKey':
                    logging.warning(f'no existing CSV file was in S3. Creating a new CSV file at {key_path}')
                else:
                    raise ce

    except Exception as e:
        logging.error(f'could not read or join any CSV: {e}')



    try:
        # making sure the csv is updated based on new data (deduplicated)
        csv_buffer = StringIO() #save data in-memeory (lambda usually is set to 512mb RAM)
        df_combined.to_csv(csv_buffer, mode='w', index=False, header=1)
        s3_client.put_object(Bucket=bucket_name, Key=key_path, Body=csv_buffer.getvalue())

    except Exception as e:
        logging.error(f'error: {e}')
