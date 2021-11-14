def getRole(message):
  roles = []
  developer = lambda x : True if "developer" in [y.name.lower() for y in message.author.roles] else False
  developer = developer(message)
  if (developer == True):
    roles.append("developer")
  nmcmanager = lambda x : True if "nmc manager" in [y.name.lower() for y in message.author.roles] else False
  nmcmanager = nmcmanager(message)
  if (nmcmanager == True):
    roles.append("nmcmanager")  
  moderator = lambda x : True if "moderator" in [y.name.lower() for y in message.author.roles] else False
  moderator = moderator(message)
  if (moderator == True):
    roles.append("moderator")
  nmcscholar = lambda x : True if "nmc scholar" in [y.name.lower() for y in message.author.roles] else False
  nmcscholar = nmcscholar(message)
  if (nmcscholar == True):
    roles.append("nmcscholar")
  admin = lambda x : True if message.author.top_role.permissions.administrator else False
  admin = admin(message)
  if (admin == True):
    roles.append("admin")

  return roles