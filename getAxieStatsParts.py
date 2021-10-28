import requests
import json

def getAxieStatsParts(axieId):

  url = "https://graphql-gateway.axieinfinity.com/graphql"

  payload = json.dumps({
    "operationName": "GetAxieDetail",
    "variables": {
    "axieId": axieId
    },
    "query": "query GetAxieDetail($axieId: ID!) {\n axie(axieId: $axieId) {\nparts {\n name \n abilities { \n name \n } \n } \n   stats { \n hp \n speed \n skill \n morale \n } \n } \n } "
  })
  headers = {
  'Content-Type': 'application/json'
}

  response = requests.request("POST", url, headers=headers, data=payload)

  # print(response.text)
  
  axie_parts = json.loads(response.text)
  parts_list = []
  for part in axie_parts['data']['axie']['parts']:
    if(len(part['abilities'])>0):
      # print(part['name'])
      # print(part['abilities'][0]['name'])
      parts_list.append({'name' : part['name'], 'card' : part['abilities'][0]['name']})
  parts_list.append({'stat' : 'hp', 'value' : axie_parts['data']['axie']['stats']['hp']})
  parts_list.append({'stat' : 'speed', 'value' : axie_parts['data']['axie']['stats']['speed']})
  parts_list.append({'stat' : 'skill', 'value' : axie_parts['data']['axie']['stats']['skill']})
  parts_list.append({'stat' : 'morale', 'value' : axie_parts['data']['axie']['stats']['morale']})
  
  return parts_list
  # data_set = {"parts": , "key2": [4, 5, 6]}

  # json_dump = json.dumps(data_set)
  
  # return embed
##


	# if response.text == "Bad Request":
	# 	return "Bad Request Sent"
	# else:
	# 	json_data = json.loads(response.text)
	# 	msg = "The current prices for requested axies are: \n\n"
	# 	count = 1
	# 	for axie in json_data["data"]["axies"]["results"]:
	# 		theString = "%d. Price: %.4f ETH / US$ %.2f Link: https://marketplace.axieinfinity.com/axie/%s/" %(count,float(axie["auction"]["currentPrice"][0:-14])/10000, float(axie["auction"]["currentPriceUSD"]),axie['id'])
	# 		msg = msg + theString + "\n"
	# 		count +=1
	# 	return msg




