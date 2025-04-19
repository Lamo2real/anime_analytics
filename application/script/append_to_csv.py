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
            df_combined = df #just incase it fails during next try

            #### merge existing data with new API fetched data ####
            try:
                s3_object = s3_client.get_object(Bucket=bucket_name, Key=key_path)
                data_from_cloud =s3_object['Body'].read().decode('utf-8')
                df_existing = pd.read_csv(StringIO(data_from_cloud))
                df_combined = pd.concat([df_existing, df], ignore_index=True) # ignore incremental id, 'concat' kinda acts like a SQL join in a way
                df_combined.drop_duplicates(subset=['anime_id', 'title'], inplace=True) # inplace indicates that it modifies the existing dataframe and doesnt create a new one

            except ClientError as ce:
                if ce.response['Error']['Code'] == 'NoSuchKey':
                    logging.info(f'no file exists on {key_path}')
                else:
                    raise ce

            for col in ['episodes', 'duration', 'genre_id_1', 'genre_id_2', 'genre_id_3']:
                if col in df_combined.columns:
                    try:
                        df_combined.loc[:, col] = df_combined[col].astype(str)
                        df_combined.loc[:, col] = df_combined[col].replace(['', 'NA', 'nan', 'None'], pd.NA)
                        df_combined.loc[:, col] = pd.to_numeric(df_combined[col], errors='coerce').astype("Int32")
                    except (ValueError, TypeError):
                        logging.warning(f'Could not convert {col} to Int32. Keeping original dtype.')
                        continue

                # making sure the csv is updated based on new data (deduplicated)
                csv_buffer = StringIO() #save data in-memeory (lambda usually is set to 512mb RAM)
                df_combined.to_csv(csv_buffer, index=False)
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=key_path,
                    Body=csv_buffer.getvalue()
                )

        except Exception as e:
            logging.error(f'could not read or join any CSV: {e}')
            return None


