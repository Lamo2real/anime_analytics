
import requests
import pandas as pd
import emoji
import re

def extract(page_number):
    """extract a page from jikan API"""

    base_rul = f'https://api.jikan.moe/v4/anime/'
    url = f'{base_rul}?page={page_number}'

    while True:
        try:
            response = requests.get(url)

            if response.status_code == 200:
                json_data = response.json()

                if not json_data['data']:
                    break

                else:
                    return json_data['data']


        except Exception as e:
            print(f'error {e}')



# additional data cleaning functions
############################################################
def remove_emojis(text):
    return emoji.replace_emoji(text, replace='')

def convert_to_minutes(duration):
    """convert hours to integers in minutes"""

    if 'hr' in duration and 'min' in duration:
        hours = re.findall(r'(\d+)\s*hr', duration)
        minutes = re.findall(r'(\d+)\s*min', duration)

        total_minutes = int(hours[0]) * 60 + int(minutes[0]) if hours and minutes else 0
        return total_minutes
    
    elif 'min' in duration:
        minutes = re.findall(r'(\d+)\s*min', duration)
        return int(minutes[0]) if minutes else 0
    
    elif 'hr' in duration:
        hours = re.findall(r'(\d+)\s*hr', duration)
        return int(hours[0]) * 60 if hours else 0
    
    else:
        return 0
    

def clean_title(text):
    """clean title of each anime for enhanced query accuracy"""

    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = remove_emojis(text)                  
    text = text.lower()                         
    text = text.replace(',', ' ')               
    text = text.replace('&', 'and')             
    text = text.replace('/', ' ')               
    text = text.replace('☆', ' ')

    return text
############################################################




def transform(i):
    """transform to showcase the data based on the KPI """

    data = extract(i)
    normalized_data = pd.json_normalize(data)
    
    

    # pd.isna() checks if the value is none
    normalized_data.dropna(subset=['title_english', 'title'], how='all', inplace=True) #drop the row if *both* are None 
    normalized_data['title_english'] = normalized_data.apply(
        lambda row: row['title'] if pd.isna(row['title_english']) else row['title_english'], axis=1
    )

    # manipulate the naming convention
    normalized_data['studio'] = (
        normalized_data['studios'].apply(
        lambda studio: studio[0]['name'] if isinstance(studio, list) and len(studio) > 0 else 'None'
    )
    .str.lower()
    )
    normalized_data[['trailer_link', 'validated', 'title', 'aired_from', 'aired_to']] = \
    normalized_data[['trailer.url', 'approved', 'title_english', 'aired.from', 'aired.to']]
    normalized_data['title'] = normalized_data['title'].apply(clean_title) # no lambda because of a row is none, code will drop the entire row
    
    # only use the first 10 characters of the string
    normalized_data[['aired_from', 'aired_to']] = normalized_data[['aired_from', 'aired_to']].apply(lambda x: x.str[:10])

    #handle episodes column data cleaning
    normalized_data['episodes'] = normalized_data['episodes'].apply(lambda x: 'None' if pd.isna(x) else int(x))

    # clean data in duration column
    if 'duration' in normalized_data.columns:
        normalized_data['duration'] = normalized_data['duration'].apply(lambda x: 'None' if pd.isna(x) else convert_to_minutes(x))
    
    
    #all elements in dataframe
    df = normalized_data[['title', 'aired_from', 'aired_to', 'episodes', 'duration', 'score', 'trailer_link', 'studio', 'validated']]
    return print(df)

    

if __name__ == "__main__":
    """runs the function locally merely if this file is run"""

    transform(113)

