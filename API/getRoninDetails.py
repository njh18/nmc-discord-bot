'''' to get their slp (function)
def get_slp(roninid):
  response = requests.get("https://game-api.axie.technology/slp/"+roninid)
  json_data = json.loads(response.text)
  ronin_id = json_data[0]['client_id']
  slp_total = json_data[0]['total']

  return(ronin_id, slp_total)

def get_mmr(roninid):
  response = requests.get("https://game-api.axie.technology/mmr/"+roninid)
  json_data = json.loads(response.text)
  ronin_id = json_data[0]['client_id']
  slp_total = json_data[0]['total']

  return(ronin_id, slp_total)
'''