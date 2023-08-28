# Created 16 Aug 2023
# Pulling data from Strava API for NLP project
# Works in tandem with NLP.ipynb 

 
import requests
import urllib3
import os
import sys
from dotenv import load_dotenv
import numpy as np 
import pandas as pd

sys.path.append('../')

#Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Get env variables

env_path = os.path.join('../.env')


load_dotenv(dotenv_path=env_path)

client_id = str(os.getenv('STRAVA_CLIENT_ID'))
client_secret = str(os.getenv('STRAVA_SECRET_CLIENT'))
michael_tok = str(os.getenv('MICHAEL_TOK'))
erika_tok = str(os.getenv('ERIKA_TOK'))
nick_tok = str(os.getenv('NICK_TOK'))

print(erika_tok)

refresh_tokens = {'Michael' : michael_tok, 
                  'Erika' :  erika_tok,
                  'Nick' : nick_tok }


#Urls 
auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

datasets = {}

for person, r_token in refresh_tokens.items():
    # Initialize the person's dataset
    datasets[person] = []
    
    for page in range(6):
        # Things we need for the API to give us the data
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': r_token,
            'grant_type': "refresh_token",
            'f': 'json'
        }

        print("Requesting Token...\n")
        res = requests.post(auth_url, data=payload)
        access_token = res.json()['access_token']
        print("Access Token = {}\n".format(access_token))

        header = {'Authorization': 'Bearer ' + access_token}
        param = {'per_page': 200, 'page': page}

        data_page = pd.json_normalize(requests.get(activites_url, headers=header, params=param).json())
        data_page['Athlete'] = person
        datasets[person].append(data_page)

# Concatenate the datasets
df = pd.concat([pd.concat(person_data, ignore_index=True) for person_data in datasets.values()], ignore_index=True)


print(df.info())