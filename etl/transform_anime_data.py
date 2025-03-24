
import logging
import pandas as pd
import time


from clean_functions import convert_to_minutes
from clean_functions import clean_title
from clean_functions import clean_genre
from clean_functions import clean_studio

from extract_anime_data import extract


def transform(i):
    """transform to showcase the data based on the KPI"""

    try:
        logging.info(f'start extraction')
        data = extract(i)
        if data:
            logging.info(f'successful data extraction')
        else:
            logging.error(f'extraction from API failed')

    except Exception as e:
        logging.critical(f'an error occured in the extraction code, {e}')
    
    finally:
        logging.info(f'end extraction')


    try:
        logging.info(f'start transformation')
        normalized_data = pd.json_normalize(data)
    
        # pd.isna() checks if the value is none
        normalized_data.dropna(subset=['title_english', 'title'], how='all', inplace=True) # drop the row if *both* are None 

        normalized_data['title_english'] = normalized_data.apply(
            lambda row: row['title'] if pd.isna(row['title_english']) else row['title_english'], axis=1
        )

        # genres organized in 3
        for i in range(1, 4):
            normalized_data[f'genre_{i}'] = normalized_data['genres'].apply(lambda genre: clean_genre(genre, i-1))

        # manipulate the naming convention
        normalized_data['studio'] = normalized_data['studios'].apply(lambda studio: clean_studio(studio))

        normalized_data[['id', 'trailer_link', 'validated', 'title', 'aired_from', 'aired_to']] = \
            normalized_data[['mal_id', 'trailer.url', 'approved', 'title_english', 'aired.from', 'aired.to']]

        normalized_data['title'] = normalized_data['title'].apply(clean_title) # no lambda because of a row is none, code will drop the entire row

        # only use the first 10 characters of the string
        normalized_data[['aired_from', 'aired_to']] = normalized_data[['aired_from', 'aired_to']].apply(lambda x: x.str[:10])

        #handle episodes column data cleaning
        normalized_data['episodes'] = normalized_data['episodes'].apply(lambda x: None if pd.isna(x) else int(x))

        # clean data in duration column
        if 'duration' in normalized_data.columns:
            normalized_data['duration'] = normalized_data['duration'].apply(lambda x: None if pd.isna(x) else convert_to_minutes(x))
        else:
            logging.error(f'no duration column was found')
        
        # remove row if aired_from is None
        normalized_data.dropna(subset=['aired_from'], how='all', inplace=True)

        # Score rounded to 1 digit (ex: 9.50 -> 9.5)
        normalized_data['score'] = round(normalized_data['score'], 1)

        #all elements in dataframe (and start from index + 1)
        df = normalized_data[['id', 'title', 'aired_from', 'aired_to', 'episodes', 'duration', 'score', 'genre_1', 'genre_2', 'genre_3', 'trailer_link', 'studio', 'validated']]
        df.index = df.index + 1

        # deduplication section
        anime_csv = 'anime_dataframe.csv'
        try:
            if pd.io.common.file_exists(anime_csv):
                df_existing = pd.read_csv(anime_csv)
                df_combined = pd.concat([df_existing, df], ignore_index=True) # ignore incremental id
                df_combined.drop_duplicates(subset=['id', 'title'], inplace=True) # inplace indicates that it modifies the existing dataframe and doesnt create a new one
            else:
                df_combined = df # merely if no existing data is true

        except Exception as e:
            logging.error(f'could not read or join the CSV: {e}')
            df_combined = df # just in case...
        
        # making sure the csv is updated based on new data (deduplicated)
        df_combined.to_csv(anime_csv, index=False)

        logging.info(f'successful data transformation for page {i}')

    except Exception as e:
        logging.error(f'error: {e}')

    finally:
        logging.info(f'end transformation')
    

if __name__ == "__main__":
    """runs the function locally merely if this file is run"""

    # transform(1)
    for i in range(1, 5):
        transform(i)
        time.sleep(3)

