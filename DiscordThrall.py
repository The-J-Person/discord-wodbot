#!/usr/bin/python3
import random
import feedparser
import time

# list of feeds to pull down
rss_feed_list = [ "https://www.reddit.com/r/WhiteWolfRPG/new.rss"
                 , "http://theonyxpath.com/feed/"
                 , "https://www.twitrss.me/twitter_user_to_rss/?user=theonyxpath" ] 

DiceLimit = 50 #Arbitrary
UpdateFrequency = 1800 #rss update frequency, in seconds

R20BNServer = '239041359384805377'
Schrecknet = '272633168178446337'
rss_chan = ['271771293739778058', '270382116322148353']

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
        
        