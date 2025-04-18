import pandas as pd
import logging
import boto3
from io import StringIO
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3 = boto3.client('s3')

def csv_logic(df, bucket_name, key_path):
    """Appends & deduplicates a DataFrame with an existing CSV in S3."""
    s3_client = S3
    df_combined = df  # Default if no existing file
    
    try:
        # 1. Try fetching existing data
        s3_object = s3_client.get_object(Bucket=bucket_name, Key=key_path)
        data_from_cloud = s3_object['Body'].read().decode('utf-8')
        
        # 2. Read CSV in chunks if large 
        df_existing = pd.read_csv(StringIO(data_from_cloud))
        
        # 3. Merge & deduplicate
        df_combined = pd.concat([df_existing, df], ignore_index=True)
        df_combined.drop_duplicates(
            subset=['anime_id', 'title'], 
            keep='last',  # or 'first'
            inplace=True
        )
        
        # 4. Fix integer columns
        int_cols = ['episodes', 'duration', 'genre_id_1', 'genre_id_2', 'genre_id_3']
        for col in int_cols:
            if col in df_combined.columns:
                df_combined[col] = pd.to_numeric(df_combined[col], errors='coerce').astype('Int64')
    
    except ClientError as e:
        if e.response['Error']['Code'] != 'NoSuchKey':
            logger.error(f"S3 error: {e}")
            raise
    except Exception as e:
        logger.error(f"CSV processing error: {e}")
        raise
    
    # 5. Upload back to S3
    try:
        csv_buffer = StringIO()
        df_combined.to_csv(csv_buffer, index=False)
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key_path,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'  # Explicit MIME type
        )
        logger.info(f"Successfully updated S3://{bucket_name}/{key_path}")
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise