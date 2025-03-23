
import emoji
import re



# additional data cleaning functions
############################################################
def remove_emojis(text):
    """replace all emojis with '' for each text"""

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
    text = text.replace(';', ':')
    text = text.replace('  ', ' ')
    text = text.strip()
    return text


def clean_genre(genre, index):
    """take the genre if it exists and make it lower case else None"""

    return genre[index]['name'].lower() if len(genre) > index else None

def clean_studio(studio):
    """return correlated data if the studio exists in a list and is larger than 0 indexes"""

    return studio[0]['name'].lower().replace(',', '') if isinstance(studio, list) and len(studio) > 0 else None
############################################################