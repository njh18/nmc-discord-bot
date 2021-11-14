from Builder.urlBuilder import urlBuilder

def getAxieSearchUrl(message):
  try:
      theString = message.content.split("$getAxieSearchUrl ", 1)[1]
      axieList = theString.split(",")
      sentMsg = ""
      for axieId in axieList:
          sentMsg = sentMsg + urlBuilder(axieId) + "\n"
      output = sentMsg
  except IndexError:
      output = "No Input given!"

  return output