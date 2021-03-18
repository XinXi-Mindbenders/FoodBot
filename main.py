import keep_alive
from datetime import datetime
import os
from PIL import Image

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
    if message.content.startswith(".stats "):
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


keep_alive.keep_alive()
client.run(TOKEN)