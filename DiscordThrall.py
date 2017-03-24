import random
import feedparser
import time
from DiscordCharacters import WoDCharacter
import os.path
from discord import message

# list of feeds to pull down
rss_feed_list = [ "https://www.reddit.com/r/WhiteWolfRPG/new.rss"
                 , "http://theonyxpath.com/feed/"
                 , "https://www.twitrss.me/twitter_user_to_rss/?user=theonyxpath" ] 

DiceLimit = 50 #Arbitrary
UpdateFrequency = 1800 #rss update frequency, in seconds

R20BNServer = '239041359384805377'
Schrecknet = '272633168178446337'
Default_Channel = '239041359384805377'
Bot_Update_Channel = '277843135193677824'
Sheets_Channel = '293805465647841280' # '276364607906643968' # Deprecated?
Announce_Channel = '239041359384805377' #'239050929716985856' # Dammit badger! :P
Gamelist_Channel = '270962496653885451'
Application_Channel = '277689369488523264'
Appquestion_Channel = '277689512992309250'
Voting_Channel = '278873402209468416'
Character_List = '293820268449628161' # This is a message ID!
rss_chan = ['271771293739778058', '270382116322148353']

class Bot():
    def __init__(self):
        self.last_updated = time.time()-UpdateFrequency
        self.sheets = {}
        for filename in os.listdir('../sheets'):
            if filename.endswith(".txt"):
                f = open('../sheets/'+filename)
                self.sheets[filename.replace('.txt','')] = WoDCharacter(f.read())
                f.close()
        
    def log(self,message):
        logfile = open('log.txt','a+')
        logtext = str(message.timestamp) + ' ' + str(message.author) + ' [' + str(message.channel) + '] ' + message.content + '\n'
        logfile.write(logtext)
        logfile.close()
        
    def exploderoll(self, faces):
        results = []
        roll = random.randrange(1,faces+1)
        results.append(roll)
        if roll==faces:
            results.append(self.exploderoll(faces))
        return results
    
    def rolldice(self, amount, faces, diff = None, botch = None, explode = False, modifier = 0, doubler = False):
        response = "("
        total = 0
        roll_results = []
        if explode:
            # Exploding die rolled recursively, like this:
            for _ in range(amount):
                for result in self.exploderoll(faces):
                    roll_results.append(result)
        else:
            # Non-exploding dice rolled like this!
            for _ in range(amount):
                roll_results.append(random.randrange(1,faces+1))
        if diff is not None:
            success = 0
            for result in roll_results:
                if result>=diff:
                    if doubler and result==faces:
                        success += 2
                        response = response + "__" + str(result) + "__ "
                    else:
                        response = response + str(result) + " "
                        success += 1
                elif botch is not None and result <= botch:
                    response = response + "**" + str(result) + "** "
                    success -= 1
                else:
                    response  = response + "~~" + str(result) + "~~ "
            response = response + ", " + str(success) + " successes)"
            total = success
        else:
            for result in roll_results:
                response = response + str(result) + " "
                total += result
        total += modifier
        if modifier == 0:
            modifier = ""
        return response + ") " + str(modifier) + " = " + str(total)
    
    def parse_dieroll(self,exp,target=None):
        try:
            if target!=None:
                target += ": `"
            else:
                target = ""
            comment = ""
            amount = 0
            faces = 0
            diff = None
            botch = None
            explode = False
            doubler = False
            modifier = 0
            the_command = ""
            the_command = exp.replace('!roll ','').replace('!r ','')
            if the_command.find('#') != -1:
                both = the_command.partition('#')
                the_command = both[0]
                comment = both[2]
            the_command = the_command.replace(' ','')
            parsed = the_command
#             print("DEBUG: Full message is " + message.content)
#             print("DEBUG: " + parsed)
            if parsed.find('s') != -1:
                both = parsed.split('s')
                doubler = True
                parsed = both[0]
            if parsed.find('-') != -1:
                both = parsed.split('-')
                modifier -= int(both[1])
                parsed = both[0]
            if parsed.find('+') != -1:
                both = parsed.split('+')
                modifier += int(both[1])
                parsed = both[0]
            if parsed.find('f') != -1:
                both = parsed.split('f')
                botch = int(both[1])
                parsed = both[0]
            if parsed.find('>=') != -1:
                both = parsed.split('>=')
                diff = int(both[1])
                parsed = both[0]
            if parsed.find('>') != -1:
                both = parsed.split('>')
                diff = int(both[1])+1
                parsed = both[0]
            if parsed.find('d') != -1:
                both = parsed.split('d')
                faces = int(both[1])
                amount = int(both[0])
                
            else:
                return "I don't see what I should roll."
            return target + the_command + '`' + comment + ' = ' + self.rolldice(amount, faces, diff, botch, explode, modifier, doubler)
        except Exception as e:
            print("DEBUG: Couldn't read roll [malformed] : " + str(e))  
            return "I didn't understand this roll request."
            pass
    
    def dice(self, message):
        self.log(message)
        the_command = message.content.replace('!roll ','').replace('!r ','')
        return self.parse_dieroll(the_command, message.author.mention)
    
    def check_role_sufficiency(self,member,role):
        roles = member.server.role_hierarchy
        roles.reverse()
        targetrole = None
        for r in roles:
            if r.name == str(role) :
                targetrole = r
        if targetrole == None:
            return None
        elif targetrole <= member.top_role:
            return True
        else:
            return False
        
    def find_role(self,server,role):
        roles = server.role_hierarchy
        roles.reverse()
        targetrole = None
        for r in roles:
            if r.name == str(role) :
                targetrole = r
        return targetrole
        
    def schrecknetpost(self, message):
        self.log(message)
        schmsg = message.content.partition(' ')[2]
        schname = "**" + schmsg.partition(' ')[0].replace('*','') + ":** "
        schmsg = schmsg.partition(' ')[2]
        return Schrecknet, schname+schmsg
    
    def give_role(self, message):
        self.log(message)
        if message.server == None:
            return "Please use this command on the server.", None
        try:
            target = message.mentions[0]
        except:
            return "I don't see who I should promote/demote.", None
        try:
            parts = message.content.split(' ')
            target_role = int(parts[2])
        except:
            return "The role to be given seems invalid.", None
        roles = message.server.role_hierarchy
        roles.reverse()
        AST = None
        for role in roles:
            if role.name == "Assistant Storyteller" :
                AST = role
        if AST == None :
            return "It seems the Assistant Storyteller role no longer exists???", None
        if message.author.top_role<AST:
            return "Only staff can promote/demote.", None
        if message.author.top_role<=roles[target_role]:
            return "You cannot promote/demote to your top role or higher", None
        # Here we know the requester has the rights to promote the requestee
        return roles[target_role], target
            
        
    def create_character(self,message):
        self.log(message)
        parts = message.content.split(' ')
        if len(parts)<2:
            return "Name missing.", None
        name = parts[1].lower()
        if os.path.isfile("../sheets/"+name+".txt"):
            return "This name is already taken. Pick another!", None
        character = WoDCharacter(name,message.author.mention)
        if len(parts)>2:
            character.template(parts[2].capitalize())
        self.character_update(character)
        self.sheets[name] = character
        return "Character created successfully.", name.capitalize()
    
    def character_update(self,character):
        charfile = open('../sheets/'+character.name+'.txt','w')
        charfile.write(str(character))
        charfile.close()
    
    def character_handling(self,message):
        self.log(message)
        parts = message.content.split(' ')
        private = False
        del parts[0]
        if len(parts)<1:
            return "Name missing.", private
        name = parts[0].lower()
        del parts[0]
        if len(parts)<1:
            return "Command missing.", private
        command = parts[0].lower()
        del parts[0]
        character = None
        for sheet in self.sheets.keys():
            if sheet == name:
                character = self.sheets[sheet]
        sheet_object = None
        if len(parts)>=1:
            sheet_object = " ".join(parts)
        response = "There was some error."
        if command=="set":
            thing = sheet_object.split(' ')[0].capitalize()
            value = sheet_object.split(' ')[1]
            if thing == "Name":
                return "Character renaming is not currently supported.", private
#                 if os.path.isfile("../sheets/"+value+".txt"):
#                     return "This name is already taken. Pick another!", private
#                 character.name = value
#                 os.rename("../sheets/"+name+".txt")
#                    # Some action to change the character list?
#                 Return "Character renamed."
            elif thing == "Owner":
                return "Character owner transfer is not currently supported.", private
            elif thing == "St" or thing == "Storyteller":
                try:
                    character.set_st = message.mentions[0].mention
                except:
                    return "Please mention the ST you wish to set for this character."
                response = "Storyteller set!"
            else:
                response = character.set_property(thing,value)
            self.character_update(character)
        elif command=="max":
            try:
                character.set_resource_capacity(sheet_object.split(' ')[0],sheet_object.split(' ')[1])
                self.character_update(character)
                response = "New maximum for " + sheet_object.split(' ')[0] + " set on " + character.name.capitalize() + "!"
            except:
                response = "Could not set capacity. Check spelling or report an error!"
        elif command=="get" or command=="show":
            private = True
            return character.get_property(sheet_object), private
        elif command=="use":
            if len(sheet_object.split(' '))>1:
                try:
                    character.consume_resource(sheet_object.split(' ')[0],sheet_object.split(' ')[1])
                except:
                    return "Error consuming this resource."
            else:
                try:
                    response = character.consume_resource(sheet_object)
                except:
                    return "Error consuming this resource."
            response = character.get_property(sheet_object.split(' ')[0])
            private = True
            self.character_update(character)
                
        elif command=="add":
            if len(sheet_object.split(' '))>1:
                try:
                    character.restore_resource(sheet_object.split(' ')[0],sheet_object.split(' ')[1])
                except:
                    return "Error replenishing this resource."
            else:
                try:
                    response = character.restore_resource(sheet_object)
                except:
                    return "Error replenishing this resource."
            response = character.get_property(sheet_object.split(' ')[0])
            private = True
            self.character_update(character)
        elif command=="reset":
            try:
                character.reset_resource(sheet_object)
            except:
                return "Error resetting this resource."
            if sheet_object.capitalize()!="Buffs":
                response = character.get_property(sheet_object.split(' ')[0])
                private = True
            else:
                response = "Buffs reset"
            self.character_update(character)
        elif command=="buff":
            response = character.add_buff(sheet_object.split(' ')[0],sheet_object.split(' ')[1])
            private = True
            self.character_update(character)
        elif command=="pickup":
            try:
                character.add_item_to_arsenal(sheet_object.split(' ')[0],sheet_object.split(' ')[1])
            except:
                return "Error completing this pick-up.", private
            response = name + "picked up a new " + sheet_object.split(' ')[0].lower() + "!"
            self.character_update(character)
        elif command=="drop":
            try:
                character.remove_item_from_arsenal(sheet_object.split(' ')[0],sheet_object.split(' ')[1])
            except:
                return "Couldn't drop this.", private
            response = name + "picked up a new " + sheet_object.split(' ')[0].lower() + "!"
            self.character_update(character)
        elif command=="roll":
            rolltext = ""
            if len(sheet_object.split(' ')) > 1:
                extras = ""
                to_roll = sheet_object.partition(' ')
                pool = str(character.get_dice_pool(to_roll[0]))
                if '>' in to_roll[2]:
                    extras = to_roll[2]
                elif 'diff' in to_roll[2]:
                    extras = ">=" + to_roll[2].replace('diff ','').split(' ')[0]
                    more = to_roll[2].partition(' ')[2]
                    if 'p' not in more:
                        extras += "f1"
                    if 'w' in more:
                        extras += "+1"
                    if 's' in more:
                        extras += "s"
                else:
                    extras = ">=6"
                    if 'p' not in to_roll[2]:
                        extras += "f1"
                    if 'w' in to_roll[2]:
                        extras += "+1"
                    if 's' in to_roll[2]:
                        extras += "s"
                rolltext = pool + "d10" + extras + " # rolling " + to_roll[0] + " for " + name
            else:
                rolltext = str(character.get_dice_pool(sheet_object)) + "d10>=6f1 # rolling " + sheet_object + " for " + name
            return self.parse_dieroll(rolltext,character.owner), private
        elif command=="extend":
            try:
                extended = sheet_object.split(' ')[0].capitalize()
                extension = sheet_object.split(' ')[1].capitalize()
                if sheet_object == "Description":
                    character.set_description(extension)
                elif sheet_object == "Statgroup":
                    character.add_stat_category(extension)
                elif sheet_object == "Resource":
                    character.create_resource(extension)
                elif sheet_object == "Arsenal":
                    character.create_arsenal(extension)
                else:
                    character.add_stat(extended,extension)
                self.character_update(character)
            except Exception as e:
                print(str(e))
                return "There was an error extending this character.", private
            response = "Extended successfully."
        else:
            return "Unrecognized command", private
        
        # Update sheet?

        return response, private
    
    def rss_ready(self):
        if time.time()>self.last_updated+UpdateFrequency:
            return True
        return False
    
    def rss_update(self,rss_history):
        if self.rss_ready():
            self.last_updated = time.time()
        else:
            return None
        updates = None
        feeds = []
        items = []
        sorted_feeditems = None
        for url in rss_feed_list:
            feeds.append(feedparser.parse(url))
        for feed in feeds:
            feeditems = []
            for item in feed["items"]:
                feeditems.append(item)
            try:
                sorted_feeditems = sorted(feeditems, key=lambda entry: entry["date_parsed"])#.reverse()[:10]
                sorted_feeditems.reverse()
                sorted_feeditems = sorted_feeditems[:10]
            except:
                try:
                    sorted_feeditems = sorted(feeditems, key=lambda entry: entry["published_parsed"])#.reverse()[:10]
                    sorted_feeditems.reverse()
                    sorted_feeditems = sorted_feeditems[:10]
                except Exception as e:
                    print("RSS Feed Error!")
                    print(e)
                    pass
                pass
            if sorted_feeditems is not None:
                for item in sorted_feeditems:
                    items.append(item)
#         sorted_items = items.sort(key=lambda r: stupidparse(r["date_parsed"]))
#         for item in items:
#             try:
#                 item["date_parsed"] = item["published_parsed"]
#         sorted_items = sorted(items, key=lambda entry: entry["date_parsed"]).reverse()[:10]
        for item in items:
            flag = True
            for message in rss_history:
                if message.content == item["link"]:
                    flag = False
            if flag == True:
                if updates is None:
                    updates = []
                updates.append(item["link"])
#         print(updates)
#         return None
        return updates
   
    def greet(self, member, chan):
        return """Welcome to Roll20 By Night!  
We are a selective Classic World of Darkness network of games that focus on high roleplay, low rollplay.  
We are happy to host Classic World of Darkness Games, and eager to grow our community.  
Please read through """ +  chan.mention + """ to learn about us and the guidelines of our server.  
When you have finished, please say 'I am ready to see the listings'
**Remove the 's.  Please note that it is case sensitive.**.
"""

#     def accept_newbie(self, member, chan):
#         return "Please review " + chan.mention + " and when you are ready, please say 'I am ready to apply to a game'"
     
    def accept_applicant(self, member, applichan ,listchan, questchan):
        return "Please review " + listchan.mention + " . If you have questions, please ask them in " + applichan.mention +""" , making sure to **mention the pertinent Storyteller @**

Once you are ready to apply for a game, please post the following in """ + applichan.mention + """:

1. Game you would like to join **(Mention the Storyteller @)**
2. Have you observed a Roll20 By Night game session yet?  If so, which game?
3. A Short background of yourself as a player
4. What type of characters and roleplay you generally enjoy

**Please note, some Storytellers make some of their text channels viewable to applicants.  If you have any questions, please ask them in """ + questchan.mention + " and mention the Storyteller.** "
    def print_info(self, message):
        try:
            what = message.content.split(' ')[1].lower()
        except:
            what = "commands"
        if what == "commands":
            return """**List of Commands:**
Replace any item in [] square brackets with appropriate content.
Content in () round brackets may be omitted. *Round brackets are not part of the command!*
            
`!help [commands/rolling/roles/voting/characters/possibly other things]` // Provides help text on the requested subject
`!r(oll) [NdN(>=NfN+N-N)]` // Rolls dice
`!sch(recknet) [name] [message]` // Sends a message to #schrecknet with the specified username.
`!promote [@user] [number]` // Adds a role (number in hierarchy) to a mentioned user. Staff only.
`!prune [@user] [number]` // Prunes the last N (number entered) messages of a user mentioned, or **offserver** for pruning messages of users who left the server. Staff only.
`!greet` // Manually initiate user application process. Should start automatically when user joins.
**Character Sheet functionality**
`!create [name] [type]` // Creates a new character sheet with the supplied name and type (ex Bob the Vampire)
`!c(har) [name] [command] [more stuff]` // Using Character Sheet functionality. See `!help characters` for more info.
"""
# + """
# **Playlist functionality** runs a process separate from the main one and, as a result, might crash independently :yum:
# `$summon` // Adds the bot to the voice room you are in. Does not work in direct-messaging!
# `$play [link]` // Plays music from given link. See https://rg3.github.io/youtube-dl/supportedsites.html for supported sites.
# `$play ytsearch:[term]` // Searches youtube for [term] and adds the first result to playing queue.
# `$pause` // Pauses audio
# `$resume` // Resumes paused
# `$stop` // Stops and clears playlist
# `$volume [number]` // Sets volume to a given percentage
# """ 
        elif what == "rolling":
            return """**Rolling**
            
Format:
`!r(oll) [AdB(>=CfD+E-Fs)]`
Rolls A dice with B faces.
Optionally, counting successes for results higher than C, 
Botching on D and lower, 
Adding E to the result and/or subtracting F from it. 
If **s** is added at the end, any maximum result will be counted as two successes.
Examples: 
`!roll 6d10>=7f1+1 `
Rolls a dice pool of six 10-sided dice at difficulty 7, subtracts any 1s from the number of successes, and adds 1 to the total (presumably willpower spent)
`!r 3d10>7`
Rolls a dice pool of three 10-sided dice at difficulty 8(>7), and doesn't substract 1s from successes rolled.
`!r 1d6-1`
Rolls one 6-sided die and subtracts 1 from the result."""
        elif what == "roles":
            hierarchy = message.server.role_hierarchy
            hierarchy.reverse()
            response = """**Server Roles:**
            
`!promote [@mention] [number]` allows a staff member to give someone a role up to their own or the bot's (whichever is lower). 
Example: `!promote @Badger 6` will give Badger role number 6.
The roles' corresponding numbers are, at present, as follows:
"""
            for i in range(1,len(hierarchy)):
                response += str(i) + '. ' + hierarchy[i].name + '\n'
            return response
        elif what == "characters":
            response = """**Character Sheet Functionality:**
            
This section is a work in progress!"""
            return response
        else:
            return "Unknown help request: Try '!help commands' for a list."
        