def roninAddConverter(roninAdd):
  if(roninAdd.startswith("ronin:")):
    return roninAdd.replace("ronin:","0x")
  elif(roninAdd.startswith("0x")):
    return roninAdd.replace("0x","ronin:")