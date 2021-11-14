from API.getGuildRonin import getGuildOwnScholarRonin, getGuildMentionScholarRonin

def myScholarRonin(message):
  ronin = 0
  # if self
  if (len(message.content.split(" ", 1)) == 1):
      ronin = getGuildOwnScholarRonin(message.author.id)
      if (ronin == None):
          output = "User not found in NMC database!"
      else:
          output = ronin

# if added a mention
  else:
      mention = message.content.split(" ", 1)[1]
      ronin = getGuildMentionScholarRonin(mention)
      if (ronin == None):
          output = "User not found in NMC database!"
      else:
          output = ronin

  return output