
import requests
import logging
import boto3

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M',
    # filename='api_logs.log'
)

def extract(page_number):
    """extract a page from jikan API"""



    base_rul = f'https://api.jikan.moe/v4/anime/'
    url = f'{base_rul}?page={page_number}'

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            logging.info(f'{response.status_code} request was succesful')
            json_data = response.json()

            if not json_data['data']:
                logging.info(f'you have reached the end')
                return json_data['data']
                
            else:
                logging.info(f'data was found')
                return json_data['data']
            
        else:
            response.raise_for_status()

    except requests.ConnectionError:
        logging.error(f'failed to connect to the server. Please check your internet connection or API URL')
    except requests.Timeout:
        logging.error(f'the API is currently unresponsive')
    except requests.HTTPError as http_e:
        logging.error(f'HTTP error: {http_e}')
    except requests.RequestException as re:
        logging.error(f'something else went wrong in the request: {re}')
    except Exception as e:
        logging.error(f'something else unrelated to HTTP request went wrong {e}')

if __name__ == '__main__':

    extract(1)