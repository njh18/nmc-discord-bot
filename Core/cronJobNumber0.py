import requests
import json
import pandas as pd
from datetime import datetime

def cronJobNumber0():
    df=pd.read_csv("./sales.csv",index_col=None)
    print("Im Scraping Data now..")
    counter = 0
    duplicate = 0
    while counter < 100:
        url = "https://graphql-gateway.axieinfinity.com/graphql"

        payload="{\"query\":\"query GetRecentlyAxiesSold($from: Int, $size: Int) {\\r\\n  settledAuctions {\\r\\n    axies(from: $from, size: $size) {\\r\\n      total\\r\\n      results {\\r\\n        ...AxieSettledBrief\\r\\n        transferHistory {\\r\\n          ...TransferHistoryInSettledAuction\\r\\n          __typename\\r\\n        }\\r\\n        __typename\\r\\n      }\\r\\n      __typename\\r\\n    }\\r\\n    __typename\\r\\n  }\\r\\n}\\r\\n\\r\\nfragment AxieSettledBrief on Axie {\\r\\n  id\\r\\n  class\\r\\n  genes\\r\\n  breedCount\\r\\n  parts {\\r\\n    ...AxiePart\\r\\n    __typename\\r\\n  }\\r\\n  stats {\\r\\n    ...AxieStats\\r\\n    __typename\\r\\n  }\\r\\n  __typename\\r\\n}\\r\\n\\r\\nfragment TransferHistoryInSettledAuction on TransferRecords {\\r\\n  total\\r\\n  results {\\r\\n    ...TransferRecordInSettledAuction\\r\\n    __typename\\r\\n  }\\r\\n  __typename\\r\\n}\\r\\n\\r\\nfragment TransferRecordInSettledAuction on TransferRecord {\\r\\n  from\\r\\n  to\\r\\n  txHash\\r\\n  timestamp\\r\\n  withPrice\\r\\n  withPriceUsd\\r\\n  fromProfile {\\r\\n    name\\r\\n    __typename\\r\\n  }\\r\\n  toProfile {\\r\\n    name\\r\\n    __typename\\r\\n  }\\r\\n  __typename\\r\\n}\\r\\n\\r\\nfragment AxiePart on AxiePart {\\r\\n  id\\r\\n  name\\r\\n  class\\r\\n  type\\r\\n  specialGenes\\r\\n  stage\\r\\n  __typename\\r\\n}\\r\\n\\r\\n\\r\\nfragment AxieStats on AxieStats {\\r\\n  hp\\r\\n  speed\\r\\n  skill\\r\\n  morale\\r\\n  __typename\\r\\n}\\r\\n\",\"variables\":{\"from\":%d,\"size\":20}}"%(counter)
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = json.loads(response.text)

        try:
            for i in json_data["data"]["settledAuctions"]["axies"]["results"]:
                if int(i["id"]) in df["axieId"].values and df[df["axieId"]==int(i["id"])]["transferHistoryCount"].values[0] == int(i["transferHistory"]["total"]):
                    duplicate += 1
                    continue
                else:
                    if i["transferHistory"]["results"][0]["timestamp"] == 0:
                        timestamp = int((datetime.now() - datetime(1970,1,1)).total_seconds())
                    else:
                        timestamp = i["transferHistory"]["results"][0]["timestamp"]
                    dictionary = {
                        "Timestamp": timestamp,
                        "axieId": i["id"],
                        "class": i["class"],
                        "genes": i["genes"],
                        "breedCount": i["breedCount"],
                        "parts": i["parts"],
                        "stats": i["stats"],
                        "transferHistoryCount": i["transferHistory"]["total"],
                        "transferHistory": i["transferHistory"],
                        }

                    df = df.append(dictionary, ignore_index=True)
            counter+=20
        except TypeError:
            print("Failed to load, trying again")
    print("Number of axies repeated: %d"%(duplicate))
    print("Im done!")
    df.to_csv("./sales.csv",index=False)