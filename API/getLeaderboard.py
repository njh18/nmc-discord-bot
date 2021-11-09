import requests
import json

def getLeaderboard(rank_offset,rank_limit):

  url = "https://game-api.axie.technology/toprank?offset=0&limit=100"

  url = "https://game-api.axie.technology/toprank?offset=" + str(rank_offset) + "&limit=" + str(rank_limit)

  payload={}
  headers = {}

  response = requests.request("GET", url, headers=headers, data=payload)

  json_data = json.loads(response.text)

  # print(json_data['items'])
  ranker_list = []
  for ranker in json_data['items']:
    ranker_list.append(ranker['client_id'])
    # ranker_list.append(ranker['rank'])

  return ranker_list