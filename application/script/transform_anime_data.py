
import logging
import pandas as pd
import os
# import time

from pd_data_structure import enhance_structure
from extract_anime_data import extract
from append_to_csv import csv_logic

def transform(event, context):
# def transform(event):
    """transform to showcase the data based on the KPI"""

    bucket_name = os.environ['BUCKET_NAME'] #referring to lambda environment variables
    s3_key_path = os.environ['S3_KEY_PATH'] #referring to lambda environment variables


    try: 
        page = event.get('page', 1) #takes page if it exists else 1
        logging.info(f'it is iterating with step functions successfully')
    except Exception as e:
        logging.error(f'something went wrong in step functions')
        raise e
    # page = event 

    ###### STFU = STep FUnction ######
    # next & run
    NEXT_RUN_STFU =  { 'continue': True, 'page': page + 1 }

    # stop & reset
    STOP_RESET_STFU = { 'continue': False, 'page': 1 }
    
    try:
        logging.info(f'start extraction')
        data = extract(page)
        normalized_data = pd.json_normalize(data)
        
            
        if not data:
            logging.info(f'no list of data left on page: {page}')
            return STOP_RESET_STFU
        
        else:
            logging.info(f'successfully extracted data from page: {page}')
            
    except Exception as e:
        logging.error(f'extraction from API failed on page: {page}: {e}')
        return STOP_RESET_STFU
        
    finally:
        logging.info(f'end extraction')


    try:
        logging.info(f'start transformation')
        normalized_data = pd.json_normalize(data)
        df = enhance_structure(normalized_data, page)
        # print(df.head(20).to_string(index=False))
        # df.to_csv('test.csv', index=False)
        csv_logic(df, bucket_name, s3_key_path)

        logging.info(f'successful data transformation for page {page}')
        return NEXT_RUN_STFU

    except Exception as e:
        logging.error(f'error: {e}')
        return STOP_RESET_STFU

    finally:
        logging.info(f'end transformation')
    



# if __name__ == "__main__":
#     """runs the function locally merely if this file is run"""

#     transform(1)
#     for i in range(1132, 1137):
#     for i in range(1, 5):
#         transform(i)
#         time.sleep(3)

