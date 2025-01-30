import requests
from config import config


 # Add necessary headers
headers = {
   'Authorization': 'Bearer ' + config.API_TOKEN,
   'Content-Type': 'application/json'
 }
 
 # Execute request
response = requests.get(config.API_TOKEN, headers=headers)
 
print(response.text)


