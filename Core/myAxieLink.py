from API.getGuildRonin import getGuildOwnRonin, getGuildMentionRonin, getGuildOwnScholarRonin

def myAxieLink(message, nmcscholar):
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
      mention = message.content.split(" ", 1)[1]
      ronin = getGuildMentionRonin(mention)
      if (ronin == None):
          output = "User not found in NMC database!"
      else:
          output = 'https://marketplace.axieinfinity.com/profile/' + ronin + '/axie/'

  return output