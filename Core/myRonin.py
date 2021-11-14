from API.getGuildRonin import getGuildOwnRonin, getGuildMentionRonin

def myRonin(message):
  ronin = 0
  # if self
  if (len(message.content.split(" ", 1)) == 1):
      ronin = getGuildOwnRonin(message.author.id)
      if (ronin == None):
          output = "User not found in NMC database!"
      else:
          output = ronin

# if added a mention
  else:
      mention = message.content.split(" ", 1)[1]
      ronin = getGuildMentionRonin(mention)
      if (ronin == None):
          output = "User not found in NMC database!"
      else:
          output = ronin

  return output