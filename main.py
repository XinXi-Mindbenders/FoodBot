from datetime import datetime
import os
from PIL import Image
from random import *
import discord
from dotenv import load_dotenv
import pickle

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
user_data = {}
if os.path.exists("data.pkl"):
    with open("data.pkl", 'rb') as f:
        user_data = pickle.load(f)
else:
    user_data = {}


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if len(message.attachments) > 0 and message.channel.id == 792317862530383893:
        for i in message.attachments:
            await i.save('out.bmp')
            try:
                img = Image.open('out.bmp')
                img.verify()
                if message.author.name in user_data:
                    user_data[message.author.name].append((i.url, datetime.now()))
                else:
                    user_data[message.author.name] = [(i.url, datetime.now())]

                with open('data.pkl', 'wb') as f:
                    pickle.dump(user_data, f)

            except Exception:
                continue
    if message.content.startswith(".stats"):
        args = message.content[7:].split(' ')
        if args[0] == 'today':
            embed = discord.Embed(title="Today's Stats:", description="View the stats for the day\n\n",
                                  color=2638993)
            for user, data in user_data.items():
                count = 1
                text_message = ""
                for img_reg in data:
                    if (datetime.now() - img_reg[1]).days == 0:
                        text_message += f'{count}. Message url: {img_reg[0]}\tTime stamp: {img_reg[1]}\n'
                        count += 1
                if text_message == "":
                    text_message = 'N/A'
                embed.add_field(name=str(user),
                                value=text_message,
                                inline=True)
            await message.channel.send(embed=embed)
        elif args[0] == 'all':
            embed = discord.Embed(title="All Time Stats:", description="View the stats for all time\n\n",
                                  color=2638993)
            for user, data in user_data.items():
                embed.add_field(name=str(user),
                                value=f'Total number of pictures sent: {len(data)}',
                                inline=True)
            await message.channel.send(embed=embed)
    if message.content.startswith(".reset"):
        args = message.content[7:].split(' ')
        with open('data.pkl', 'wb') as f:
            pickle.dump(user_data, f)
        if len(args) > 1:
            if len(message.mentions) > 0:
                for mem in message.mentions:
                    user_data[mem.name] = []
                embed = discord.Embed(title="Success!",
                                      color=2638993)
                embed.add_field(name='Reset ✅',
                                value=f'The user data has been reset for: {[member.name for member in message.mentions]}\n\n',
                                inline=True)
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title="Error!",
                                      color=2638993)
                embed.add_field(name='Reset ❌',
                                value='''Incorrect arguments passed. This function needs the user being reset to be mentioned.\n\nTip:\nYou can reset everyone using '.reset' with no arguments and you can reset multiple people by mentioning multiple people''',
                                inline=True)
                await message.channel.send(embed=embed)
        else:
            for user in user_data:
                user_data[user] = []
            embed = discord.Embed(title="Success!",
                                  color=2638993)
            embed.add_field(name='Reset ✅',
                            value='The user data for all users has been reset.\n\n',
                            inline=True)
            await message.channel.send(embed=embed)
        with open('data.pkl', 'wb') as f:
            pickle.dump(user_data, f)
    if message.content.startswith(".minus"):
        args = message.content[7:].split(' ')
        print(len(args))
        if len(args) < 2:
            embed = discord.Embed(title="Error!", color=2638993)
            embed.add_field(name='Reset ❌', value='''Incorrect arguments passed. This function needs the user being 
            reset to be mentioned.\n\nTip:\n do .minus <number> [mentions]''', inline=True)
            await message.channel.send(embed=embed)
        else:
            toRemove = int(args[0])
            for mem in message.mentions:
                if (len(user_data[mem.name]) <= toRemove):
                    user_data[mem.name] = []
                else:
                    user_data[mem.name] = user_data[mem.name][0:-1 * toRemove]
            embed = discord.Embed(title="Success!",
                                  color=2638993)
            embed.add_field(name='Reset ✅',
                            value=f'The users {[member.name for member in message.mentions]} have lost their past {toRemove} entrys.\n\n',
                            inline=True)
            await message.channel.send(embed=embed)

    if message.content.startswith(".help"):
        await message.channel.send("my name is Nathaniel and I hate help menues")
    if message.content.startswith(".tiebreak"):
        leastFood = len(user_data[0])
        toBreak = []
        for user in user_data:
            leastFood = min(leastFood, len(user_data[user]))
        for user in user_data:
        	if len(user_data[user]) == leastFood:
        		toBreak.append(user)
        embed = discord.Embed(title="Success!" ,color=2638993)
        embed.add_field(name='Reset ✅', value=f'Out of the losers {[member.name for member in toBreak]}, {toBreak[random() * len(toBreak)]} has lost.\n\n', inline=True)
        await message.channel.send(embed=embed)        



client.run(TOKEN)
