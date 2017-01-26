#!/usr/bin/python3
class Current_User():
    def __init__(self, json):
        self.id = json['id']
        self.name = json['username']
        self.avatar_url = json['avatar_image_url']
        self.profile_url = ""
        self.ascendant = json['is_ascendant']
        self.last_activity = ""
        self.utc_timezone = json['utc_offset']
        self.lang = json['locale']
        self.created = ""
        self.updated = ""
        self.campaigns = []
        for game in json['campaigns']:
            self.campaigns.append((game["id"],game["name"],game["role"]))
    def get_GM_campaigns(self):
        gmcamps = []
        for game in self.campaigns:
            if game[2]=='game_master' or game[2]=='co_game_master':
                gmcamps.append(game)

class Campaign():
    def __init__(self, identity, charindex, wikiindex):
        self.id = identity[0]
        self.name = identity[1]
        self.accesslevel = identity[2]
        self.characters = charindex
        self.wikipages = wikiindex

class Character():
    def __init__(self, charjson):
        self.id = charjson['id']
        self.name = charjson['name']
    
class WikiPage():
    def __init__(self):
        pass