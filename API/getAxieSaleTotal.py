import requests
import json


def getAxieSaleTotal():
	url = "https://graphql-gateway.axieinfinity.com/graphql"

	payload="{\"query\":\"query GetAxieBriefList(\\r\\n  $auctionType: AuctionType\\r\\n  $criteria: AxieSearchCriteria\\r\\n  $from: Int\\r\\n  $sort: SortBy\\r\\n  $size: Int\\r\\n  $owner: String\\r\\n) {\\r\\n  axies(\\r\\n    auctionType: $auctionType\\r\\n    criteria: $criteria\\r\\n    from: $from\\r\\n    sort: $sort\\r\\n    size: $size\\r\\n    owner: $owner\\r\\n  ) {\\r\\n    total\\r\\n  }\\r\\n}\\r\\n\\r\\n\",\"variables\":{\"from\":0,\"size\":1,\"sort\":\"PriceAsc\",\"auctionType\":\"Sale\",\"criteria\":{}}}"
	headers = {
		'Content-Type': 'application/json'
	}

	response = requests.request("POST", url, headers=headers, data=payload)

	json_data = json.loads(response.text)
	
	return json_data["data"]["axies"]["total"]

