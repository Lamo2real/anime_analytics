
import emoji
import re
import logging
import pandas as pd



# additional data cleaning functions
############################################################
def remove_emojis(text):
    """replace all emojis with '' for each text"""

    return emoji.replace_emoji(text, replace='')

def convert_to_minutes(duration, page):
    """convert hours & minutes to integers in minutes"""

    try:
        total_minutes = 0
        if 'hr' in duration and 'min' in duration:
            hours = re.findall(r'(\d+)\s*hr', duration)
            minutes = re.findall(r'(\d+)\s*min', duration)
            total_minutes = int(hours[0]) * 60 + int(minutes[0]) if hours and minutes else 0

            return total_minutes

        elif 'min' in duration:
            minutes = re.findall(r'(\d+)\s*min', duration)
            total_minutes = int(minutes[0]) if minutes else 0

            return total_minutes

        elif 'hr' in duration:
            hours = re.findall(r'(\d+)\s*hr', duration)
            total_minutes = int(hours[0]) * 60 if hours else 0

            return total_minutes
        
        elif 'sec' in duration:
            seconds = re.findall(r'(\d+)\s*sec', duration)
            total_minutes_exact = int(seconds[0]) / 60 if seconds else 0
            total_minutes = round(total_minutes_exact, 2)

            return total_minutes
         
        else:
            return pd.NA
    
    except Exception as e:
        logging.warning(f'something else went wrong: {e}')
        return pd.NA
    

def clean_title(text):
    """clean title of each anime for enhanced query accuracy"""

    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = remove_emojis(text)                  
    text = text.lower()                         
    text = text.replace(',', ' ')               
    text = text.replace('&', 'and')             
    text = text.replace('/', ' ')               
    text = text.replace('☆', ' ')
    text = text.replace(';', ':')
    text = text.replace('  ', ' ')
    text = text.strip()
    return text

############################################################
