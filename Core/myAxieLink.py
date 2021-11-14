from API.getGuildRonin import getGuildOwnRonin, getGuildMentionRonin, getGuildOwnScholarRonin, getGuildMentionScholarRonin

def myAxieLink(message, nmcscholar, admin, nmcmanager, developer, moderator):
  ronin = 0
  # if self
  if (len(message.content.split(" ", 1)) == 1):
    if(nmcscholar):
      ronin = getGuildOwnScholarRonin(message.author.id)
    else:
      ronin = getGuildOwnRonin(message.author.id)
      if (ronin == None):
          output = "User not found in NMC database!"
      else:
          # await message.channel.send(ronin)
          output = 'https://marketplace.axieinfinity.com/profile/' + ronin + '/axie/'

# if added a mention
  else:
    if (admin or nmcmanager or developer or moderator or message.author.id == 772847165550755900):
      mention = message.content.split(" ", 1)[1]
    if(len(list(filter(lambda x : x.name.lower() == "nmc scholar", message.mentions[0].roles)))>0):
      ronin=getGuildMentionScholarRonin(message.mentions[0].id)
    else:
      ronin = getGuildMentionRonin(mention)
      # mention = message.content.split(" ", 1)[1]
      # ronin = getGuildMentionRonin(mention)
      if (ronin == None):
          output = "User not found in NMC database!"
      else:
          output = 'https://marketplace.axieinfinity.com/profile/' + ronin + '/axie/'

  return output