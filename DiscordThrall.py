#!/usr/bin/python3
import random
import feedparser
import time

rss_feed_list = [ "https://www.reddit.com/r/WhiteWolfRPG/new.rss" ] # list of feeds to pull down

DiceLimit = 50 #Arbitrary
UpdateFrequency = 1800 #rss update frequency, in seconds

Server = None
Schrecknet = None
rss_chan = None
Instance = None

def stupidparse(tup):
    return tup[5]+tup[4]*100+tup[3]*10000+tup[2]*1000000+tup[1]*100000000+tup[0]*10000000000

class Bot():
    def __init__(self):
        global Instance 
        Instance = self
        self.last_updated = time.time()-UpdateFrequency
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
    def rss_update(self,rss_history):
        if time.time()>self.last_updated+UpdateFrequency:
            self.last_updated = time.time()
        else:
            return None
        updates = None
        feeds = []
        items = []
        for url in rss_feed_list:
            feeds.append(feedparser.parse(url))
        for feed in feeds:
            for item in feed["items"]:
                items.append(item)
#         sorted_items = items.sort(key=lambda r: stupidparse(r["date_parsed"]))
        sorted_items = sorted(items, key=lambda entry: entry["date_parsed"])
        for item in sorted_items:
            flag = True
            for message in rss_history:
                if message.content == item["link"]:
                    flag = False
            if flag == True:
                if updates is None:
                    updates = []
                updates.append(item["link"])
        return updates
        
        