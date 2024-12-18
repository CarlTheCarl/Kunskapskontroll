import requests
import json
import csv
import logging
import time
import sys

logging.basicConfig(
    filename= 'logfile.log',
    format='[%(asctime)s][%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M' #code is supposed to only run once per day so second/millisecond granularity is unecessary
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#url = 'https://api.scryfall.com/cards/44dcab01-1d13-4dfc-ae2f-fbaa3dd35087'
base_url = 'https://api.scryfall.com/cards'
user_agent_name = {'User-Agent':'MTG Elesh Norn Mother of Machines Price Tracker/0.2'}

def scryfall_card_fetch(mtgcard):
    url = f"{base_url}/{mtgcard}"
    time.sleep(0.1) #Scryfall requests a 50-100 milisecond wait between responses, this is here to ensure that
    logger.debug('Sending REST Request to %s using User-Agent %s', url, user_agent_name)
    response = requests.get(url, headers=user_agent_name, verify=True) #scryfall requires API requests to be handled through HTTPS
    if response.status_code == 200:
        logger.info('Card info sucessfully retrieved, HTTP Code: %d', response.status_code)
        card_info = response.json()
        return card_info
    else:
        logger.critical('FATAL ERROR: Card not retrieved, HTTP Code: %d', response.status_code)
        sys.exit('Card Fetch Failed HTTP Code: %d', response.status_code)

card_id = '44dcab01-1d13-4dfc-ae2f-fbaa3dd35087'
card_info = scryfall_card_fetch(card_id)

#logger.info('Sum of %d and %d is %d', i, j, mult_sum)