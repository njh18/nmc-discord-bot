from API.getGuildRonin import getGuildOwnRonin, getGuildMentionRonin, getGuildOwnScholarRonin, getGuildMentionScholarRonin

def mySLP(message, roles):  
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
      output = "Let me make a quick trip down to Lunacia to retrieve that information!"

  # if added a mention
  else:
      # if admin, get ronin of mentioned
      permissions = ['admin', 'nmcmanager', 'developer', 'moderator']
      if (any(role in permissions for role in roles) or message.author.id == 772847165550755900):
        mention = message.content.split(" ", 1)[1]
        if(len(list(filter(lambda x : x.name.lower() == "nmc scholar", message.mentions[0].roles)))>0):
          ronin=getGuildMentionScholarRonin(message.mentions[0].id)
        else:
          ronin = getGuildMentionRonin(mention)
        if (ronin == 0):
          output = "User not found in NMC database!"
        else:
          output = "Let me make a quick trip down to Lunacia to retrieve that information!"
      else:
          output = "Mind your own business."
  
  return output, ronin