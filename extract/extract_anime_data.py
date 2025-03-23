
import requests

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
                    print(f'you have reached the end')
                    break

                else:
                    return json_data['data']


        except Exception as e:
            print(f'error {e}')
