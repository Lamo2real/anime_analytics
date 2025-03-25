import pandas as pd
import logging
import os
import warnings

def csv_logic(df):
        """join the new dataframe and existing dataframe into one, then update csv"""

      # deduplication section
        anime_csv = 'anime_dataframe.csv'
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=FutureWarning)
                
                if os.path.exists(anime_csv):
                    df_existing = pd.read_csv(anime_csv)
                    df_combined = pd.concat([df_existing, df], ignore_index=True) # ignore incremental id, 'concat' kinda acts like a SQL join in a way
                    df_combined.drop_duplicates(subset=['id', 'title'], inplace=True) # inplace indicates that it modifies the existing dataframe and doesnt create a new one
                else:
                    df_combined = df # merely if no existing data is true

        except Exception as e:
            logging.warning(f'could not read or join any CSV: {e}')
            df_combined = df # just in case...

        try:
            # making sure the csv is updated based on new data (deduplicated)
            df_combined.to_csv(anime_csv, index=False)
            logging.info(f"CSV file updated successfully.")
        
        except Exception as e:
            logging.error(e)
