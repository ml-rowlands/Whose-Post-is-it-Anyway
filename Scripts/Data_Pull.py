#Import everything I will need for this 
import requests
import urllib3
import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#from pandas.io.json import json_normalize
import datetime as dt
from scipy.optimize import curve_fit
import scipy.stats as stats



#Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


refresh_tokens = {'Michael' : '321e0aa1e8e17d37b2867e4752aa43766474cd3a', 
                  'Erika' :   '59df18fe42368e80e13b9686284333be69e872a2'
                    }


#Urls 
auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

datasets = {}

for person, r_token in refresh_tokens.items():
  
#Things we need for the API to give us the data
  payload = {
      'client_id': "75238", 
      'client_secret': '0ad2c3b5d522ef8f4dbbb89d4759efabea4f7ff6',
      'refresh_token': r_token,

      'grant_type': "refresh_token",
      'f': 'json'
  }

  print("Requesting Token...\n")
  res = requests.post(auth_url, data=payload, verify=False)
  access_token = res.json()['access_token']
  print("Access Token = {}\n".format(access_token))

  header = {'Authorization': 'Bearer ' + access_token}
  param = {'per_page': 200, 'page': 1}

  datasets[person] = pd.json_normalize(requests.get(activites_url, headers=header, params=param).json())
  datasets[person]['Athlete'] = person
  
  
datasets


df = pd.concat(datasets.values(), ignore_index=True)
