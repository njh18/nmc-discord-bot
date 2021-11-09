import json
import requests

def getAxieDetail(ronin):
  url = "https://axie-infinity.p.rapidapi.com/get-axies/" + ronin

  headers = {
      'x-rapidapi-host': "axie-infinity.p.rapidapi.com",
      'x-rapidapi-key': "0ef48ec908msh1d9fe1ea269f91ep1c3345jsn05ea39c25075"
      }
  response = requests.request("GET", url, headers=headers)
  json_data = json.loads(response.text)

  return json_data['data']['axies']['results']