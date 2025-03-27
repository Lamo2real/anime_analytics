
import logging
import pandas as pd
import time
import os
from dotenv import load_dotenv

from pd_data_structure import enhance_structure
from extract_anime_data import extract
from append_to_csv import csv_logic

load_dotenv()

def transform(event, context):
    """transform to showcase the data based on the KPI"""

    bucket_name = os.getenv('BUCKET_NAME')
    s3_key_path = os.getenv('S3_KEY_PATH')
    page = event.get('page', 1) #takes page if it exists else 1
    
    try:
        logging.info(f'start extraction')
        data = extract(page)
        normalized_data = pd.json_normalize(data)
        
        if data:
            logging.info(f'successfully extracted data from page: {page}')
        elif not data:
            logging.info(f'no list of data left on page: {page}')
            return {
                'continue': False,
                'page': page
            }
        else:
            logging.error(f'extraction from API failed on page: {page}')
            
    except Exception as e:
        logging.error(f'an error occured in the extraction code on page: {page}, {e}')
        
    finally:
        time.sleep(3)
        logging.info(f'end extraction')


    try:
        logging.info(f'start transformation')
        normalized_data = pd.json_normalize(data)
        df = enhance_structure(normalized_data, page)
        
        csv_logic(df, bucket_name, s3_key_path)

        logging.info(f'successful data transformation for page {page}')
        return {
            'continue': True,
            'page': page + 1
        }

    except Exception as e:
        logging.error(f'error: {e}')

    finally:
        logging.info(f'end transformation')
    



if __name__ == "__main__":
    """runs the function locally merely if this file is run"""

    transform()
    # for i in range(1132, 1137):
    # for i in range(1, 5):
        # transform(i)
        # time.sleep(3)

