import requests
import json

def urlBuilder(axieId):

    url = "https://graphql-gateway.axieinfinity.com/graphql"
    
    payload = json.dumps({
      "operation": "GetAxieDetail",
      "variables": {
        "axieId": axieId
      },
      "query": "query GetAxieDetail($axieId: ID!) { axie(axieId: $axieId) { ...AxieDetail __typename } } fragment AxieDetail on Axie { id class parts { ...AxiePart __typename } stats { ...AxieStats } __typename } fragment AxiePart on AxiePart { id type __typename } fragment AxieStats on AxieStats { hp speed skill morale }"
    })
    headers = {
      'Content-Type': 'application/json'
    }

    
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.text == "Bad Request":
        return "Axie Id not found"
    else:
        json_data = json.loads(response.text)["data"]["axie"]
        baseUrl = "https://marketplace.axieinfinity.com/axie/?"
        
        baseUrl = baseUrl + "class=" + json_data["class"] + "&"
        
        for part in json_data["parts"]:
            if part["type"] not in ("Eyes","Ears"):
                baseUrl = baseUrl + "part=" + part["id"] + "&"
                
        for key in json_data["stats"]:
            value = json_data["stats"][key]
            baseUrl = baseUrl + key + "=" + str(value) + "&" + key + "=61&" 

    
        return baseUrl[:-1]