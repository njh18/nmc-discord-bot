from API.getGuildRonin import getGuildOwnRonin, getGuildMentionRonin, getGuildOwnScholarRonin, getGuildMentionScholarRonin

def myMMR(message, roles):  
  ronin = 0
  # if self
  if (len(message.content.split(" ", 1)) == 1):
    if('nmcscholar' in roles):
      ronin = getGuildOwnScholarRonin(message.author.id)
    else:
      ronin = getGuildOwnRonin(message.author.id)
    if (ronin == None):
      output = "User not found in NMC database!"
    else:
      output = "Hold on, let me ask ma boy Neph."

# if added a mention
  else:
    permissions = ['admin', 'nmcmanager', 'developer', 'staff', 'coach']
    if (any(role in permissions for role in roles) or message.author.id == 772847165550755900 or message.author.id == 789023396733255680):
      mention = message.content.split(" ", 1)[1]
      if(len(list(filter(lambda x : x.name.lower() == "nmc scholar", message.mentions[0].roles)))>0):
        ronin=getGuildMentionScholarRonin(message.mentions[0].id)
      else:
        ronin = getGuildMentionRonin(mention)
      if (ronin == 0):
        output = "User not found in NMC database!"
      else:
        output = "Hold on, let me ask ma boy Neph."
    else:
      output = "Mind your own business."

  return output, ronin