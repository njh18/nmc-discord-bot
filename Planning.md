# Database Planning

Since its a Key-Value store, i think we can store multiple "tables" to fit the different requests we need.

So there will be 3 different Layers of the Dictionary

	First Layer: The Different "Tables"

	Second Layer: The Managers (so we got our own scholars ronin)

	Third Layer: Specific details like ronin addresses etc


Can refer to **Database Schema.json** for an example

# Permissions 

1.	I think can somehow grant permissions for some functions, need to see the Message Class

	a.	[API Reference](https://discordpy.readthedocs.io/en/stable/api.html#message)

	b.	I think can track the sender so if sender is one of us then the function runs. Like the message.author think

	c. prevent random scholar to add or remove ronins

# Functions Needed

### Ronin & SLP related

1.	Add new ronin ID under a Manager into Database

	a.	$functionName [Manager] [ScholarName] [RoninAdd]

2. Remove ronin ID based on ScholarName or Ronin Add

	a. $functionName [ScholarName]/[RoninAdd]

3. Get total SLP for 1 scholar based on Ronin add/ ScholarName

4. Get total SLP for scholars under 1 Manager

5. Get total SLP for all scholars under MNC

### Filter & Axie Price related

1. Add criteria into Database

2. See a list of criterias

3. Get prices based on 1 criteria (either URL or Name of criteria)

	a. should we get top 5 or top 10 hmm 10 seems like alot 

4. Edit/Delete criteria

5. Get prices for all criterias 

6. Given a List of Axie IDs, get back the query
