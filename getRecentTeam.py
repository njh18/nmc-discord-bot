import requests
import json
from getAxieStatsParts import getAxieStatsParts


def getRecentTeam(ronin):

  url = "https://game-api.axie.technology/battlelog/" + str(ronin)
    
  payload={}
  headers = {}
  response = requests.request("GET", url, headers=headers, data=payload)
  json_data = json.loads(response.text)

  try:
    client_id = ''
    if(str(ronin) == json_data[0]['items'][0]['first_client_id']):
      client_id=json_data[0]['items'][0]['first_team_id']
    else:
      client_id=json_data[0]['items'][0]['second_team_id']

    axielist = []
    for fighter in json_data[0]['items'][0]['fighters']:
      if(fighter['team_id']==client_id):
        axie_stats_parts = {"id" :  fighter['fighter_id'], "class" :  fighter['fighter_class'], "statsParts" : getAxieStatsParts(fighter['fighter_id'])}
        axielist.append(axie_stats_parts)
    print(axielist)
    return axielist
  except:
    return None

