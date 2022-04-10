import discord
import asyncio
import json
from Builder.roninAddConverter import roninAddConverter

async def onboard(message, roles, client): 
  permissions = ['admin', 'nmcmanager', 'developer']
  if (any(role in permissions for role in roles)):
      if (len(message.content.split(" ", 1)) == 1):
          await message.channel.send(
              "Incorrect onboarding command. Please mention the scholar after \'$onboard\'")
      else:
          mention = message.content.split(" ", 1)[1].replace('@', '').replace(
              '<', '').replace('>', '').replace('!', '')
          print(mention)

        # Check Name
        
          # embed = discord.Embed(title="Please input the scholar's name",
          #                       color=0x66a1a5)
          # message3 = await message.channel.send(embed=embed)

          # max_timer = 30
          # check_timer = 0
        
          # scholarname = 0
          # while (check_timer < max_timer):
          #     print('waiting for scholar name')
          #     # await asyncio.sleep(5)
          #     try:
          #         msg2 = await client.wait_for('message', timeout=5)
          #     except:
          #         print('waited 5s for scholar name')
          #         check_timer += 5
          #         print(check_timer)
          #         continue
          #     print(msg2.content)
          #     message2fetch = msg2.content
          #     # message2fetch = await message.channel.fetch_message(message2)

          #     print(check_timer)
          # if (scholarname == 0):
          #     message1 = await message.channel.send(
          #         'No input received. Timing out.'
          #     )
          #     return
          # else:
          #     print("clan : " + clan)
          #     print("ronin : " + str(ronin))
          #     new_scholar = {
          #         "userId": int(mention),
          #         "managerShare": 5,
          #         "eth": "",
          #         "name": str(message.mentions[0].name),
          #         "scholarRonin": ronin,
          #         "investorPercentage": "",
          #         "investorRonin": ""
          #     }

          # Check Name End
          # Check Clan

          clan_emojis = [
              '\N{Palm Tree}', '\N{Last Quarter Moon with Face}',
              '\N{Hot Beverage}', '\N{Glowing Star}'
          ]
          clan_names = [
              'oasis',
              'lunar',
              'kopi',
              'sol',
          ]

          embed = discord.Embed(title="Please react to the clan you wish to onboard this scholar to.",
                                color=0x66a1a5)
          message1 = await message.channel.send(embed=embed)
          for emoji in clan_emojis:
              await message1.add_reaction(emoji)

          max_timer = 30
          check_timer = 0

          clan_emoji = 0
          clan = 0

          while (check_timer < max_timer):
              print('waiting to react to clan')
              await asyncio.sleep(5)
              message1fetch = await message.channel.fetch_message(
                  message1.id)
              print('waited to react to clan')
              for reaction in message1fetch.reactions:
                  print(reaction.count)
                  if (reaction.count == 2):
                      clan_emoji = reaction.emoji
                      clan = clan_names[clan_emojis.index(clan_emoji)]
                      # await message.channel.send('New scholar is from ' + clan + ' clan.')
                      await message.channel.send('\n Input received : ' +
                                                  clan.capitalize() +
                                                  ' clan. \n')
                      check_timer = max_timer
              check_timer += 5
              print(check_timer)
          if (clan == 0):
              message1 = await message.channel.send(
                  'No input received. Please try to \'$onboard\' again.')
              return

# Check Clan End
# Check Ronin

          embed = discord.Embed(title="Please input the scholar's GAME ACCOUNT ronin (not his/her own)",
                                color=0x66a1a5)
          message2 = await message.channel.send(embed=embed)

          check_timer = 0
          ronin = 0
          while (check_timer < max_timer):
              print('waiting for ronin input')
              # await asyncio.sleep(5)
              try:
                  msg2 = await client.wait_for('message', timeout=5)
              except:
                  print('waited 5s for ronin input')
                  check_timer += 5
                  print(check_timer)
                  continue
              print(msg2.content)
              message2fetch = msg2.content
              # message2fetch = await message.channel.fetch_message(message2)

              if (message2fetch.startswith('ronin:')):
                  ronin = message2fetch
                  print(ronin)
                  break
              elif (message2fetch.startswith('0x')):
                  ronin = roninAddConverter(message2fetch)
                  print(ronin)
                  break
              else:
                  await message.channel.send(
                      'This is not an acceptable ronin format. Ronin wallet starts with \'0x\' or \'ronin:\'')
                  check_timer = 0
                  print('timer reset')
              print(check_timer)
          if (ronin == 0):
              message1 = await message.channel.send(
                  'No input received. Timing out.'
              )
              return
          else:
              print("clan : " + clan)
              print("ronin : " + str(ronin))
              new_scholar = {
                  "userId": int(mention),
                  "managerShare": 5,
                  "eth": "",
                  "name": str(message.mentions[0].name),
                  "scholarRonin": ronin,
                  "investorPercentage": "",
                  "investorRonin": ""
              }
            
          confirm_emojis = [
              '\N{White Heavy Check Mark}', '\N{Cross Mark}'
          ]

          embed = discord.Embed(
              title="Kindly confirm the details of new scholar",
              color=0x66a1a5).add_field(
                  name="Discord Name : ",
                  value=str(message.mentions[0].name),
                  inline=False).add_field(
                      name="Clan : ",
                      value=clan.capitalize(),
                      inline=False).add_field(
                          name="User ID : ",
                          value=str(mention),
                          inline=False).add_field(
                              name="Ronin Address : ",
                              value=ronin,
                              inline=False)
          message3 = await message.channel.send(embed=embed)
          for emoji in confirm_emojis:
              await message3.add_reaction(emoji)

          max_timer = 30
          check_timer = 0

          clan_emoji = 0
          scholarConfirmed = False

          while (check_timer < max_timer):
              print('waiting to confirm')
              await asyncio.sleep(5)
              message3fetch = await message.channel.fetch_message(
                  message3.id)
              print('waited to confirm')
              for reaction in message3fetch.reactions:
                  if (reaction.count == 2):
                      if (reaction.emoji == '\N{White Heavy Check Mark}'
                          ):
                          # scholarConfirmed=True
                          with open("Database-ronin.json",
                                    "r") as jsonFile:
                              dbRonin = json.load(jsonFile)
                          dbRonin["roninAdd"][clan].append(new_scholar)
                          with open("Database-ronin.json",
                                    "w") as jsonFile:
                              json.dump(dbRonin, jsonFile)
                          await message.channel.send(embed=discord.Embed(
                              title=
                              "Success! Scholar has been onboarded to NMC Database.",
                              color=0x1abb9c))
                          return
                      elif (reaction.emoji == '\N{Cross Mark}'):
                          await message.channel.send(embed=discord.Embed(
                              title=
                              "Scholar Onboarding Cancelled. Please try \'$onboard\' again.",
                              color=0xec4543))
                          return
                      check_timer = max_timer
              check_timer += 5
              print(check_timer)
          if (clan == 0):
              message1 = await message.channel.send(
                  'No input received. Please try to \'$onboard\' again.')
              return