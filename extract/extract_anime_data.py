
import requests
import pandas as pd
import time
import os

def extract(anime_id):
    
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            response_data = response.json()
            normalized_data = pd.json_normalize(response_data['data'])
            formatted_data = pd.DataFrame(normalized_data)
            formatted_data['studios_name'] = formatted_data['studios'].apply(lambda x: x[0]['name'] if isinstance(x, list) & len(x) > 0 else None)
            formatted_data['aired_from'] = formatted_data['aired.from']
            formatted_data['aired_to'] = formatted_data['aired.to']
            formatted_data['trailer_url'] = formatted_data['trailer.url']
            formatted_data['genre'] = formatted_data['genres'].apply(lambda x: x[0]['name'] if isinstance(x, list) & len(x) > 0 else None)

            df = formatted_data[['title_english', 'episodes',
                                'duration', 'score', 'aired_from',
                                'aired_to', 'url', 'trailer_url',
                                'studios_name', 'approved' ]]
            
            csv_file_exists = os.path.exists('anime_data.csv')
            df.to_csv('anime_data.csv', mode='a', index=True, header=not csv_file_exists)

            return print(df)
        
        elif response.status_code == 404:
            error_response = response.json()
            error_data_status = error_response['status']
            error_data_message = error_response['message']
            return print(f'{error_data_status}, Anime Not Found/{error_data_message}')
        
        elif response.status_code == 500:
            return print(f'Internal Server Error. The developers are on it, please try again later.')
        else:
            return print(f'something weird went wrong...')
    
    except Exception as e:
        print(f'error {e}')
        return
    
if __name__ == "__main__":
    """runs the function locally merely if this file is run"""

    id = 1
    for i in range(id, 15):
        extract(i)
        time.sleep(2)
