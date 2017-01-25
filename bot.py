import discord
import DiscordThrall  
from keyring import *  # @UnusedWildImport

client = discord.Client()
Bot = DiscordThrall.Bot()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    for server in client.servers:
        for channel in server.channels:
            if channel.name == 'schrecknet':
                DiscordThrall.Schrecknet = channel
                DiscordThrall.Server = server
    

@client.event
async def on_message(message):
    destination = None
    response = None
    if message.content.startswith('!test'):
        return
#         counter = 0
#         tmp = await client.send_message(message.channel, 'Calculating messages...')
#         async for log in client.logs_from(message.channel, limit=100):
#             if log.author == message.author:
#                 counter += 1
#  
#         await client.edit_message(tmp, 'You have {} messages.'.format(counter))
#     elif message.content.startswith('!sleep'):
#         await asyncio.sleep(5)
#         await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!introduce yourself'):
        await client.send_message(message.channel, 'Hello, I am your humble servant.')
    elif message.content.startswith('!roll '):
        destination, response = Bot.schrecknetpost(message)
    elif message.content.startswith('!schrecknet '):
        destination, response = Bot.schrecknetpost(message)
    else:
        return
    await client.send_message(destination, response)

client.run(DiscordToken)









