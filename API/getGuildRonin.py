from replit import db
import re # to search for digit

clans = ['oasis', 'kopi', 'lunar', 'sol', 'singapore']

def getGuildOwnRonin(guildMember):
	for clan in clans:
    # print(clan)
		for user in db["roninAdd"][clan]:
			userId = user["userId"]
			if(userId==guildMember):
				if(user["eth"]!=""):
					return user["eth"]
				else:
					return "Your ronin address has not been added to database!"

def getGuildMentionRonin(mentionedMember):

	if(type(mentionedMember)==str):  
		mentionedMember = mentionedMember.replace('@', '')
		mentionedMember = mentionedMember.replace('<', '')
		mentionedMember = mentionedMember.replace('>', '')
		mentionedMember = mentionedMember.replace('!', '')

	print(mentionedMember)
	userid = int(mentionedMember)
	# userid = int(mentionedMember[int(offset)+1:-1])
	print(userid)
	for clan in clans:
		for user in db["roninAdd"][clan]:
			userId = user["userId"]
			if(userId==userid):
				if(user["eth"]!=""):
					return user["eth"]
				else:
					return "Your ronin address has not been added to database!"

def getGuildOwnScholarRonin(guildMember):
	for clan in clans:
    # print(clan)
		for user in db["roninAdd"][clan]:
			userId = user["userId"]
			if(userId==guildMember):
				if(user["scholarRonin"]!=""):
					return user["scholarRonin"]
				else:
					return "Hmm.. You don't seem to be a scholar."

def getGuildMentionScholarRonin(mentionedMember):

	if(type(mentionedMember)==str):  
		mentionedMember = mentionedMember.replace('@', '')
		mentionedMember = mentionedMember.replace('<', '')
		mentionedMember = mentionedMember.replace('>', '')
		mentionedMember = mentionedMember.replace('!', '')

	print(mentionedMember)
	userid = int(mentionedMember)
	# userid = int(mentionedMember[int(offset)+1:-1])$
	print(userid)
	for clan in clans:
		for user in db["roninAdd"][clan]:
			userId = user["userId"]
			if(userId==userid):
				if(user["scholarRonin"]!=""):
					return user["scholarRonin"]
				else:
					return "Hmm.. You don't seem to be a scholar."