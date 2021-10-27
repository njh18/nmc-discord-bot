import json

# This function is used to build the criteria json file for the graphql endpoint

# Input : url
# output : criteria/filter in JSON format

def criteriaBuilder(url):
    baseUrl= "https://marketplace.axieinfinity.com/axie/?"
    baseCriteria = {
        "classes": [],
        "parts": [],
        "pureness": [],
        "numMystic": [],
        "stages": [],
        "breedCount": [],
        "speed": [],
        "hp": [],
        "skill": [],
        "morale":[]	
    }

    url = url.replace(baseUrl,"")
    criterias = url.split("&")
    for criteria in criterias:
        item = criteria.split("=")
        if item[0] == "class":
            baseCriteria["classes"].append(item[1])
        elif item[0] == "stage":
            baseCriteria["stages"].append(int(item[1]))
        elif item[0] == "part":
            baseCriteria["parts"].append(item[1])
        elif item[0] == "mystic":
            baseCriteria["numMystic"].append(int(item[1]))
        elif item[0] in ["pureness","breedCount","hp","skill","speed","morale"]:
            baseCriteria[item[0]].append(int(item[1]))

    return baseCriteria
