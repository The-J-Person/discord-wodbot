import random

DiceLimit = 50 #Arbitrary

Server = None
Schrecknet = None
Instance = None

class Bot():
    def __init__(self):
        global Instance 
        Instance = self
    def log(self,message):
        logfile = open('log.txt','a+')
        logtext = str(message.timestamp) + ' ' + str(message.author) + ' [' + str(message.channel) + '] ' + message.content + '\n'
        logfile.write(logtext)
        logfile.close()
    def rolldice(self, message):
        self.log(message)
        try:
            result=""
            part = message.content.split()[1]
            parts = part.split('d')
            partnums = [int(parts[0]), int(parts[1])]
            for _ in range(partnums[0]):
                randomnum = random.randrange(1,partnums[1]+1)
                result = result + str(randomnum) + ','
            return message.channel, result
        except:
            return message.channel, "I didn't understand that one, sorry :("
            pass
    def schrecknetpost(self, message):
        self.log(message)
        schmsg = message.content.partition(' ')[2]
        schname = "**" + schmsg.partition(' ')[0].replace('*','') + ":** "
        schmsg = schmsg.partition(' ')[2]
        return Schrecknet, schname+schmsg
        