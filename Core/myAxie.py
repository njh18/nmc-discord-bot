from Builder.roninAddConverter import roninAddConverter
from API.getAxieDetail import getAxieDetail
from API.getGuildRonin import getGuildOwnRonin, getGuildOwnScholarRonin, getGuildMentionScholarRonin, getGuildMentionRonin

def myAxie(message, nmcscholar):
  ronin = 0
  output = ""
# if self
  if (len(message.content.split(" ", 1)) == 1):
    if(nmcscholar):
      ronin = getGuildOwnScholarRonin(message.author.id)
    else:
      ronin = getGuildOwnRonin(message.author.id)
      if (ronin == None):
          output = "User not found in NMC database!"
          return      

# if added a mention
  else:
      mention = message.content.split(" ", 1)[1]
      if(len(list(filter(lambda x : x.name.lower() == "nmc scholar", message.mentions[0].roles)))>0):
        ronin=getGuildMentionScholarRonin(message.mentions[0].id)
      else:
        ronin = getGuildMentionRonin(mention)
        if (ronin == 0):
          output = "User not found in NMC database"
          return
          
# first level check for noob axie message
  ronin = roninAddConverter(ronin)
  return output, getAxieDetail(ronin)