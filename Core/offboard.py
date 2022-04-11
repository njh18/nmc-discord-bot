import discord
import json
import asyncio
from Core.dbUpdate import dbUpdate

async def offboard(message, roles):
  permissions = ['admin', 'nmcmanager', 'developer']
  if (any(role in permissions for role in roles)):
      if (len(message.content.split(" ", 1)) == 1):
          await message.channel.send(
              "Can mention him/her after \'$offboard\'?")
      else:
        clan_emojis = ['\N{Palm Tree}', '\N{Last Quarter Moon with Face}', '\N{Hot Beverage}', '\N{Glowing Star}']
        clan_names = ['oasis', 'lunar', 'kopi', 'sol']

        embed = discord.Embed(title="This paikia what clan one?", color=0x66a1a5)
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
                    await message.channel.send('\n Input received : ' +
                                                clan.capitalize() +
                                                ' clan. \n')
                    check_timer = max_timer
            check_timer += 5
            print(check_timer)
        if (clan == 0):
            message1 = await message.channel.send(
                'No input received. Please try to \'$offboard\' again.')
            return
        
        mentionID = message.mentions[0].id
        print(mentionID)
        with open("Database-ronin.json", "r") as jsonFile:
          dbRonin = json.load(jsonFile)
        for scholar in dbRonin['roninAdd'][clan]:
          if (scholar['userId'] == mentionID):
            confirm_emojis = ['\N{White Heavy Check Mark}', '\N{Cross Mark}']
            embed = discord.Embed(
                title="Kindly confirm the details of scholar to offboard",
                color=0x66a1a5).add_field(
                    name="Discord Name : ",
                    value=str(message.mentions[0].name),
                    inline=False).add_field(
                        name="Clan : ",
                        value=clan,
                        inline=False).add_field(
                            name="User ID : ",
                            value=str(mentionID),
                            inline=False).add_field(
                                name="Ronin Address : ",
                                value=scholar['scholarRonin'],
                                inline=False)
            message2 = await message.channel.send(embed=embed)
            for emoji in confirm_emojis:
                await message2.add_reaction(emoji)

            max_timer = 30
            check_timer = 0

            clan_emoji = 0

            while (check_timer < max_timer):
              print('waiting to confirm')
              await asyncio.sleep(5)
              message2fetch = await message.channel.fetch_message(message2.id)
              print('waited to confirm')
              for reaction in message2fetch.reactions:
                  if (reaction.count == 2):
                    if (reaction.emoji == '\N{White Heavy Check Mark}'):
                      dbRonin['roninAdd'][clan].pop(dbRonin['roninAdd'][clan].index(scholar))
                      with open("Database-ronin.json", "w") as jsonFile:
                        dbRonin = json.dump(dbRonin, jsonFile)
                      await message.channel.send(embed=discord.Embed(
                            title=
                            "Success! Scholar has been offboarded from NMC Database.",
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
              message1 = await message.channel.send('No input received. Please try to \'$offboard\' again.')

        await message.channel.send('Scholar not found!')
        return