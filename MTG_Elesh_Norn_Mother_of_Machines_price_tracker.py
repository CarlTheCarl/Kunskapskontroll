import requests
import json
import csv
import logging

logging.basicConfig(
    filename= 'logfile.log',
    format='[%(asctime)s][%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M' #code is supposed to only run once per day so second/millisecond granularity is unecessary
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

url = 'http://httpbin.org/headers' #placeholder url for debugging purposes
user_agent_name = {'User-Agent':'MTG Elesh Norn Mother of Machines Price Tracker/0.1'}

#logger.info('Sum of %d and %d is %d', i, j, mult_sum)
#TODO: Bake the JSON fetching into a function
logger.info('Sending REST Request to %s using User-Agent %s', url, user_agent_name)
response = requests.get(url, headers=user_agent_name)

if response.status_code == '200':
    logger.info('Card info sucessfully retrieved, HTTP Code: %d', response.status_code)
else:
    logger.critical('FATAL ERROR: Card not retrieved, HTTP Code: %d', response.status_code)

print(response.status_code) #Temporary code for debugging purposes
print(response.text)