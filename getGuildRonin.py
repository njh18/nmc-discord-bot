from replit import db
import re # to search for digit

clans = ['oasis', 'kopi', 'lunar', 'sol']

def getGuildOwnRonin(guildMember):
	for clan in clans:
    # print(clan)
		for user in db["roninAdd"][clan]:
			userId = user["userId"]
			if(userId==guildMember):
				return user["eth"]

def getGuildMentionRonin(mentionedMember):
	# for i, c in enumerate(mentionedMember):
	# 	if c.isdigit():
	# 		offset = c
	# 		break
	# adminDelimiter = mentionedMember.search('!')
	# print(adminDelimiter)

	# if(adminDelimiter==None):
	# 	offset = adminDelimiter + 1
	# else:
	# 	offset = mentionedMember.search('@') + 1

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
				return user["eth"]