#!/usr/bin/python3
import discord
import DiscordThrall
import logging
from keyring import *  # @UnusedWildImport

client = discord.Client()
Bot = DiscordThrall.Bot()

@client.event
async def wait_until_ready():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.WARNING)
    handler = logging.FileHandler(filename='bot_technical.loggimm', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#When someone joins the server
# @client.event
# async def on_member_join(member):
#     server = member.server
#     fmt = 'Welcome {0.mention} to {1.name}!'
#     await client.send_message(server, fmt.format(member, server))

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
        
    # Rolling
    elif message.content.startswith('!r ') or message.content.startswith('!roll '):
        destination, response = Bot.dice(message)
        
    # Schrecknet
    elif message.content.startswith('!sch ') or message.content.startswith('!schrecknet  '):
        destination, response = Bot.schrecknetpost(message)
        
    # Pruning
    elif message.content.startswith('!prune '):
        destination = message.channel.id
        if Bot.check_role_sufficiency(message.author, "Assistant Storyteller") == None:
            response = "Something is wrong with the Role Hierarchy."
        elif Bot.check_role_sufficiency(message.author, "Assistant Storyteller") == False:
            response = "Only staff can prune messages."
        else:
            try:
                try:
                    target = message.mentions[0]
                except:
                    return "I don't see a target mentioned."
                try:
                    parts = message.content.split(' ')
                    num_to_prune = int(parts[2])
                except:
                    return "The amount to prune seems invalid"
                history = []
                
                async for msg in client.logs_from(message.channel, limit=500):
                    if msg.author == target:
                        history.append(msg)
                sorted_history = sorted(history, key=lambda entry: entry.timestamp)
                sorted_history.reverse()
                
                for msg in sorted_history[:num_to_prune]:
                    await client.delete_message(msg)
                response = "Pruned successfully."
            except:
                response = "Some messages couldn't be deleted."
            
    # Role adding
    elif message.content.startswith('!promote '):
        destination = message.channel.id
        role, target = Bot.give_role(message)
        if target is not None:
            try:
                await client.add_roles(target,role)
                response = message.mentions[0].name + " has been granted the role of " + role.name + "!"
            except Exception as e:
                print(e)
                response = "I was unable to complete this promotion :'("
        else:
            response = role
    
    # Help requests
    elif message.content.startswith('!help '):
        destination = message.channel.id
        response = Bot.print_info(message)   
    
    # Blank help request 
    elif message.content == 'help!':
        destination = message.channel.id
        response = Bot.print_info(message)
        
    # Character sheet creation
    elif message.content.startswith('!create '):
        destination = message.channel.id
        response, sheet = Bot.create_character(message)
        await client.send_message(client.get_channel(DiscordThrall.Sheets_Channel), sheet)
        
    # Character sheet functionality
    elif message.content.startswith('!char '):
        destination = message.channel.id
        sheets = []
        async for msg in client.logs_from(client.get_channel(DiscordThrall.Sheets_Channel), limit=500):
            sheets.append(msg)
        response, newsheet, oldsheet = Bot.character_handling(message,sheets)
        if newsheet is not None:
            await client.edit_message(oldsheet, newsheet)
        
    else:
        return
    chan = client.get_channel(destination)
    await client.send_message(chan, response)
    
    
@client.event
async def on_member_join(member):
    if member.server != client.get_server(DiscordThrall.R20BNServer):
        return
    infochannel = client.get_channel(DiscordThrall.Fledglings_Channel)
    await client.send_message(infochannel, 
                              "Welcome to " + member.server.name + ", " + member.name + 
                              "!  Please check out the pins in " + infochannel.mention + 
                              " .  It explains about us and how to get into a game!")
    
@client.event
async def on_member_remove(member):
    if member.server != client.get_server(DiscordThrall.R20BNServer):
        return
    infochannel = client.get_channel(DiscordThrall.Fledglings_Channel)
    await client.send_message(infochannel, member.name + " has left the server.")
        
@client.event
async def on_typing(channel,user,when):
    if not Bot.rss_ready():
        return
    logs = []
    # Everything here is a dirty, inefficient hack. Optimize it!
    for ch_id in DiscordThrall.rss_chan:
        chan = client.get_channel(ch_id)
        async for message in client.logs_from(chan, limit=50):
            logs.append(message)
    rssupdates = Bot.rss_update(logs)
    if rssupdates is not None:
        for update in rssupdates:
            for ch_id in DiscordThrall.rss_chan:
                chan = client.get_channel(ch_id)
                await client.send_message(chan,update)
                
def prune(message):

    return sorted_history[:num_to_prune]
            
client.run(DiscordToken)









