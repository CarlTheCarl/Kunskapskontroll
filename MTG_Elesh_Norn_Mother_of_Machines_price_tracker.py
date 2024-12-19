import requests
import json
import csv
import logging
import time
import sys
import os
from datetime import date

logging.basicConfig(
    filename= 'logfile.log',
    format='[%(asctime)s][%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M' #code is supposed to only run once per day so second/millisecond granularity is unecessary
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#url = 'https://api.scryfall.com/cards/44dcab01-1d13-4dfc-ae2f-fbaa3dd35087'
base_url = 'https://api.scryfall.com/cards'
user_agent_name = {'User-Agent':'MTG Elesh Norn Mother of Machines Price Tracker/0.3'} #scryfall requires the user-agent to be named after its specific purpose

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
        logger.critical('FATAL ERROR: Card not retrieved, HTTP Code: %d', response.status_code)
        sys.exit('Card Fetch Failed HTTP Code: %d', response.status_code)

card_id = '44dcab01-1d13-4dfc-ae2f-fbaa3dd35087'
card_info = scryfall_card_fetch(card_id)
print(card_info['prices'])
print(card_info['name'])

# csv_dictionary = {}
# csv_dictionary['name'] = card_info['name']
# price_info = card_info['prices']
# for price_type in price_info:
#     csv_dictionary[price_type] = price_info[price_type]
# csv_dictionary['date_retrieved'] = date.today()

csv_list = []
csv_list.append(card_info['name'])
price_info = card_info['prices']
for price_type in price_info:
    print(price_info[price_type])
    csv_list.append(price_info[price_type])
csv_list.append(date.today())

if os.path.exists('Elesh_Norn_Price_History.csv'):
    with open('Elesh_Norn_Price_History.csv', mode='a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_list)
else:
    with open('Elesh_Norn_Price_History.csv', mode='w') as csvfile:
        fieldnames = ['name', 'usd', 'usd_foil', 'usd_etched', 'eur', 'eur_foil', 'tix', 'date_retrieved']
        writer = csv.writer(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(csv_list)
#TODO: fix the append part of the csv writing script

#logger.info('Sum of %d and %d is %d', i, j, mult_sum)