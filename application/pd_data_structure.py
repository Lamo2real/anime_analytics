
import logging
import pandas as pd

from clean_functions import convert_to_minutes, clean_title, clean_genre, clean_studio

def enhance_structure(dataset, page):

    # pd.isna() checks if the value is none
        dataset.dropna(subset=['title_english', 'title'], how='all', inplace=True) # drop the row if *both* are None 

        dataset['title_english'] = dataset.apply(
            lambda row: row['title'] if pd.isna(row['title_english']) else row['title_english'], axis=1
        )

        # genres organized in 3
        for i in range(1, 4):
            dataset[f'genre_{i}'] = dataset['genres'].apply(lambda genre: clean_genre(genre, i-1))

        # manipulate the naming convention
        dataset['studio'] = dataset['studios'].apply(lambda studio: clean_studio(studio))

        dataset[['id', 'trailer_link', 'validated', 'title', 'aired_from', 'aired_to']] = \
            dataset[['mal_id', 'trailer.url', 'approved', 'title_english', 'aired.from', 'aired.to']]

        dataset['title'] = dataset['title'].apply(clean_title) # no lambda because of a row is none, code will drop the entire row

        # only use the first 10 characters of the string
        dataset[['aired_from', 'aired_to']] = dataset[['aired_from', 'aired_to']].apply(lambda x: x.str[:10])

        #handle episodes column data cleaning
        dataset['episodes'] = dataset['episodes'].apply(lambda x: None if pd.isna(x) else int(x))

        # clean data in duration column
        if 'duration' in dataset.columns:
            dataset['duration'] = dataset['duration'].apply(lambda x: None if pd.isna(x) else convert_to_minutes(x, page))
        else:
            logging.error(f'no duration column was found')

        # remove row based on attributes
        dataset.dropna(subset=['aired_from', 'score', 'duration'], how='any', inplace=True)

        # Score rounded to 1 digit (ex: 9.50 -> 9.5)
        dataset['score'] = round(dataset['score'], 1)

        #all elements in dataframe (and start from index + 1)
        df = dataset[[
            'id', 'title', 'aired_from',
            'aired_to', 'episodes', 'duration',
            'score', 'genre_1', 'genre_2', 'genre_3',
            'trailer_link', 'studio', 'validated'
            ]]
        df.index = df.index + 1

        return df