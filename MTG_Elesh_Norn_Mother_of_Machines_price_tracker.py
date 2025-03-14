import requests
import logging
import time
import sys
import os
import pandas
from datetime import date

logging.basicConfig(
    filename= 'logfile.log',
    format='[%(asctime)s][%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M' #code is supposed to only run once per day so second/millisecond granularity is unecessary
)
logger = logging.getLogger()
logger.setLevel(logging.WARNING)

base_url = 'https://api.scryfall.com/cards'
user_agent_name = {'User-Agent':'MTG Elesh Norn Mother of Machines Price Tracker/1.0.1'} #scryfall requires the user-agent to be named after its specific purpose

def scryfall_card_fetch(mtgcard):
    url = f"{base_url}/{mtgcard}"
    time.sleep(0.1) #Scryfall requests a 50-100 milisecond wait between responses, this is here to ensure that
    logger.debug('Sending REST Request to %s using User-Agent %s', url, user_agent_name)
    response = requests.get(url, headers=user_agent_name, verify=True) #scryfall requires API requests to be handled through HTTPS
    if response.status_code == 200:
        card_info = response.json()
        logger.info('MTG Card: %s sucessfully retrieved, HTTP Code: %d',card_info['name'], response.status_code)
        return card_info
    else:
        logger.critical('FATAL ERROR: Card could not be retrieved, HTTP Code: %d', response.status_code)
        sys.exit('Card Fetch Failed HTTP Code: %d', response.status_code)

card_id = '44dcab01-1d13-4dfc-ae2f-fbaa3dd35087' #scryfall allows for multiple search type, i went with id because it felt the most secure
card_info = scryfall_card_fetch(card_id)

csv_dictionary = {}
csv_dictionary['name'] = card_info['name']
price_info = card_info['prices']
for price_type in price_info: #scryfall bundles all the prices in a nested dictionary, this is to unwrap that
    if price_info[price_type] != None:
        csv_dictionary[price_type] = float(price_info[price_type]) #ensures that price is stored as a float
    else:
        csv_dictionary[price_type] = price_info[price_type]
csv_dictionary['date_retrieved'] = date.today()

fieldnames = ['name', 'usd', 'usd_foil', 'usd_etched', 'eur', 'eur_foil', 'tix', 'date_retrieved']
df = pandas.DataFrame(csv_dictionary, index=fieldnames)
df = df.drop_duplicates() #TODO: fix so that this isn't needed
if os.path.exists('Elesh_Norn_Price_History.csv'):
    df.to_csv('Elesh_Norn_Price_History.csv',mode='a', header=False, sep=';', decimal =',', index=False)
else:
    df.to_csv('Elesh_Norn_Price_History.csv', header=fieldnames, sep=';', decimal =',', index=False)