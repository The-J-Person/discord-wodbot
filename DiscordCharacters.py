def sortkey(label):
    if label=="Nature" or label=="Physical" or label=="Breed" or label=="Willpower":
        return 0
    elif label=="Demeanor" or label=="Social" or label=="Auspice":
        return 1
    elif label=="Clan" or label=="Mental" or label=="Tribe":
        return 2
    elif label=="Talent":
        return 3
    elif label=="Skill":
        return 4
    elif label=="Knowledge":
        return 5
    elif label=="Discipline":
        return 6
    elif label=="Background":
        return 7
    elif label=="Description" or label=="Item":
        return 500
    return 10

# So should I go for [Ж] Agg [X] Lethal [/] Bashing [ ] OK ???
def damage_char(text):
    text = text.lower()
    if text == "aggravated" or text == "agg" or text == "a":
        return 'Ж'
    elif text == "lethal" or text == "l":
        return 'X'
    elif text == "bashing" or text == "bash" or text == "b":
        return '/'
    else:
        return ' '
    
def damage_sort(char):
    if char == 'Ж':
        return 1
    elif char == 'X':
        return 2
    elif char == '/':
        return 3
    elif char == ' ':
        return 4
    else:
        return 0
    
def penalty_sort(text):
    try:
        return int(text)
    except:
        pass
    return 10

class WoDCharacter:
    def __init__(self, text=None, owner=None):
        self.name = text
        self.owner = owner
        self.st = None
        self.health = ['∅']
        self.damage = [' ']
        self.descriptions = {}
        self.desclist = []
        self.stats = {}
        self.statlist = [[]]
        self.buffs = {}
        self.resources = {}
        self.resourcelist = []
        self.arsenals = {}
        self.arslist = []
        if text!=None and owner==None:
            self.initialize_from_string(text)
    def __str__(self,):
        return "---\n".join(self.to_text_section(0))
    def status(self):
        result = "**Name:** " + self.name + "\n**Health:**\n```C\n"
        for level in self.health:
            result += '[' + str(level) + ']'
        result += "\n"
        for level in self.damage:
            result += '[' + str(level) + ']'
        result += '\n```\n'
        for buff in self.buffs.keys():
            if buff not in self.resourcelist:
                result += self.get_property(buff) + "\n"
        for resource in self.resourcelist:
            result += self.get_property(resource) + "\n"
        return result
    def display(self):
        section = []
        fullname = ""
        try:
            fullname = self.descriptions["Character Name"]
        except:
            pass
        result = "__Identification__\n**Name:** " + self.name + "\n**Character Name:** " \
        + fullname + "\n**Owner:** <@" + self.owner +">\n**Storyteller**: <@" + str(self.st) + ">\n" \
        + "\n**Health:**\n```C\n"
        for level in self.health:
            result += '[' + str(level) + ']'
        result += "\n"
        for level in self.damage:
            result += '[' + str(level) + ']'
        result += '\n```\n'
        section.append(result)#result += "---\n"
        
        result = "__Descriptions__\n"
        for description in self.desclist:
            if description == "Character Name":
                continue
            result += "**" + description + ":** " + self.descriptions[description] + "\n"
        section.append(result)#result += "---\n"
        result = "__Stats__\n"
        for i in range(len(self.statlist[0])):
            result += "__**" + self.statlist[0][i] + ":**__\n"
            for stat in self.statlist[i+1]:
                if stat in self.buffs:
                    result += "**" + stat + ":** " + str(self.stats[self.statlist[0][i]][stat]) + "(" + str(self.stats[self.statlist[0][i]][stat]+self.buffs[stat]) +")\t"
                else:
                    result += "**" + stat + ":** " + str(self.stats[self.statlist[0][i]][stat]) + "\t"
            result += "\n"
        section.append(result)#result += "---\n"
        result = "__Resources__\n"
        for resource in self.resourcelist:
            if resource in self.buffs:
                result += "**" + resource + ":** " + str(self.resources[resource][0]) + "/" + str(self.resources[resource][1]) + "(" + str(self.resources[resource][1]+self.buffs[resource]) + ")\n"
            else:
                result += "**" + resource + ":** " + str(self.resources[resource][0]) + "/" + str(self.resources[resource][1]) + "\n"
        section.append(result)#result += "---\n"
        result = "__Collections__\n"
        for bag in self.arslist:
            result += "**" + bag + ":** "
            for item in self.arsenals[bag]:
                result += item + ", "
            result = result.strip(', ')
            result+="\n"
        result = result.strip('\n')
        section.append(result)
        return "---\n".join(section)
    def to_text_section(self,limit=2000): #Discord Message Length Limit is 2000. This is now addressed in another file.
        # Thus, this function's 'limit' features serve no purpose.
        section = []
        result = "**Name:** " + self.name + "\n**Owner:** " + self.owner +"\n**Storyteller**: " \
        + str(self.st) + "\n**Health Levels** \t"
        incap_damage = self.damage[len(self.damage)-1]
        del self.damage[len(self.health)-1]
        self.health.remove('∅')
        for level in self.health:
            result += str(level) + ','
        result = result.strip(',')
        result += "\n**Damage:** \t\t"
        for level in self.damage:
            result += str(level) + ','
        result = result.strip(',')
        result += "\n"
        section.append(result)#result += "---\n"
        result = ""
        for description in self.desclist:
            result += "**" + description + ":** " + self.descriptions[description] + "\n"
        section.append(result)#result += "---\n"
        result = ""
        for i in range(len(self.statlist[0])):
            result += "__**" + self.statlist[0][i] + ":**__\n"
            for stat in self.statlist[1+i]:
                result += "**" + stat + ":** " + str(self.stats[self.statlist[0][i]][stat]) + "\t"
            result += "\n"
        section.append(result)#result += "---\n"
        result = ""
        for resource in self.resourcelist:
            result += "**" + resource + ":** " + str(self.resources[resource][0]) + "/" + str(self.resources[resource][1]) + "\n"
        section.append(result)#result += "---\n"
        result = ""
        for bag in self.arslist:
            result += "**" + bag + ":** "
            for item in self.arsenals[bag]:
                result += item + ", "
            result = result.strip(', ')
            result+="\n"
        result = result.strip('\n')
        section.append(result)
        self.damage.append(incap_damage)
        self.health.append('∅')
        self.health.sort(key=penalty_sort, reverse=False)
        return section
    def set_name(self,name):
        self.name = name
    def set_owner(self,owner):
        self.owner = owner
    def set_st(self,st):
        self.st = st
    def add_health_level(self,penalty):
        self.health.append(int(penalty))
        self.health.sort(key=lambda h: penalty_sort(h), reverse=False)
        self.damage.append(' ')
    def heal_damage(self, t = None):
        response = ""
        if t is None:
            if '/' in self.damage:
                self.damage.remove('/')
                response = "bashing"
            elif 'X' in self.damage:
                self.damage.remove('X')
                response = "lethal"
            elif 'Ж' in self.damage:
                self.damage.remove('Ж')
                response = "aggravated"
            else:
                return "ERROR: No damage to heal."
        else:
            t = damage_char(t)
            if t not in self.damage:
                return "ERROR: No damage of the specified type on this character."
            self.damage.remove(t)
            response = "Healed this type of damage."
        self.damage.append(' ')
        self.damage.sort(key=damage_sort, reverse=False)
        return response
            
    def take_damage(self,t):
        t = damage_char(t)
        if ' ' in self.damage:
            self.damage.remove(' ')
            self.damage.append(t)
        elif '/' in self.damage:
            self.damage.remove('/')
            if t == '/':
                self.damage.append('X')
            else:
                self.damage.append(t)
        elif 'X' in self.damage:
            self.damage.remove('X')
            self.damage.append('Ж')
        else:
            return "**" + self.name.capitalize() + "'s Health:**\n" + self.show_health()
            + "This is final death, *or* maybe you're beating a dead horse."
        self.damage = sorted(self.damage, key=lambda k: damage_sort(k))
        response = self.show_health()
        if ' ' not in self.damage:
            if '/' in self.damage or 'Ж' not in self.damage:
                response += "\n *This character is incapacitated.*"
            elif 'X' in self.damage and 'Ж' in self.damage:
                response += "\n *If mortal, this character is dead.*" #Ask badger whether this is the case
            else:
                response += "\n *This character is dead. Convert to* **Wraith the Oblivion** *sheet?*"
        return response
    def show_health(self):
        result = self.name.capitalize() + "'s **health**:\n```C\n"
        for level in self.health:
            result += '[' + str(level) + ']'
        result += "\n"
        for level in self.damage:
            result += '[' + str(level) + ']'
        result += '\n```'
        return result
    def remove_health_level(self,penalty):
        self.health.remove(int(penalty))
        del self.damage[len(self.health)]
        self.health.sort(key=penalty_sort, reverse=False)
    def add_description(self,desc):
        if desc is None or len(desc)<1:
            return "ERROR: Description missing."
        desc = desc.capitalize()
        if desc in self.desclist:
            return "ERROR: Already exists."
        self.desclist.append(desc)
        self.descriptions[desc] = ""
        return desc + "added to " + self.name.capitalize() + "'s description list."
    def remove_description(self,desc):
        if desc is None or len(desc)<1:
            return "ERROR: Description missing."
        desc = desc.capitalize()
        if desc not in self.desclist:
            return "ERROR: Description not on character."
        del self.descriptions[desc]
        self.desclist.remove(desc)
        return "Removed successfully."
    def set_description(self,desc,content):
        self.descriptions[desc.capitalize()] = content
        return desc.capitalize() + " set for " + self.name + "!"
    def add_stat_category(self,cat_name):
        if cat_name.capitalize() in self.stats:
            return "Already exists."
        self.statlist[0].append(cat_name.capitalize())
        self.statlist.append([])
        self.stats[cat_name.capitalize()] = {}
        return "Created successfully."
    def add_stat(self, category, name):
        category = category.capitalize()
        name = name.capitalize()
        if category not in self.stats:
            return "You don't have such a stat category."
        if name in self.stats[category]:
            return "This stat already exists."
        index = self.statlist[0].index(category)+1
        self.statlist[index].append(name)
        self.stats[category][name] = 0
        return "Created successfully."
    def remove_stat(self, stat):
        key = ""
        cat = ""
        for category in self.stats.keys():
            for entry in self.stats[category].keys():
                if entry == stat.capitalize():
                    key = entry
                    cat = category
                    break
            if key != "":
                break
        if key == "":
            return "The character lacks this stat.\n*Check spelling?."
        del self.stats[cat][key]
        self.statlist[self.statlist[0].index(cat)+1].remove(key)
        return stat.capitalize() + " has been removed."
    def set_stat(self,stat,level):
        key = ""
        cat = ""
        for category in self.stats.keys():
            for entry in self.stats[category].keys():
                if entry == stat.capitalize():
                    key = entry
                    cat = category
                    break
            if key != "":
                break
        if key == "":
            return "The character lacks this stat.\n*Check spelling or add a new stat*."
        self.stats[cat][key] = int(level)
        return stat.capitalize() + " set to " + str(level) + " for " + self.name + "!"
    def get_numeric_stat(self,stat):
        key = ""
        cat = ""
        stat = stat.capitalize()
        try:
            n = int(stat)
            return n
        except:
            pass
        for category in self.stats.keys():
            for entry in self.stats[category].keys():
                if entry == stat.capitalize():
                    key = entry
                    cat = category
                    break
            if key != "":
                break
        if key == "":
            for entry in self.resources.keys():
                if entry == stat.capitalize():
                    key = entry
                    cat = "resource"
                    break
        if key == "":
            return "The character lacks this stat or resource.\n*Check spelling or add a new one*."
        total = 0
        if cat != "resource":
            total += self.stats[cat][stat]
        else:
            total +=self.resources[stat][1]
        try:
            total += self.buffs[stat]
        except:
            pass
        return total
    def get_dice_pool(self,stats):
        if isinstance(stats, str):
            stats = stats.split('+')
        total = 0
        for stat in stats:
            total += self.get_numeric_stat(stat)
        return total
    def get_dice_penalty(self):
        c = 0
        for dot in self.damage:
            if dot != ' ':
                c += 1
        if c == len(self.health):
            return -1
        if c == 0:
            return 0
        return self.health[c-1]
    def create_resource(self,rsrc):
        rsrc = rsrc.capitalize()
        if len(rsrc) < 1:
            return "ERROR: Resource not found"
        if rsrc in self.resourcelist:
            return "ERROR: Already exists"
        self.resourcelist.append(rsrc)
        self.resources[rsrc.capitalize()] = [1,1]
        return "Created successfully."
    def remove_resource(self,rsrc):
        rsrc = rsrc.capitalize()
        if len(rsrc) < 1:
            return "ERROR: Resource not found in request"
        if rsrc not in self.resourcelist:
            return "ERROR: Resource not on character"
        del self.resources[rsrc.capitalize()]
        self.resourcelist.remove(rsrc)
        return "Resource deleted."
    def set_resource(self,rsrc,amount):
        self.resources[rsrc.capitalize()][0] = int(amount)    
        return rsrc + " set to " + str(amount) + "/" + str(self.resources[rsrc][1]) + " for " + self.name + "!"
    def set_resource_capacity(self,rsrc,amount):
        self.resources[rsrc.capitalize()][1] = int(amount)
        return self.name.capitalize() + "'s " + rsrc.capitalize() + " has been set to a maximum of " + str(amount)
    def consume_resource(self,rsrc,amount=1):
        self.resources[rsrc.capitalize()][0] -= int(amount)
        return self.name.capitalize() + " spent " + str(amount) + " " + rsrc.capitalize() + """.
Now at""" + self.resources[rsrc.capitalize()][1] + "/" + self.resources[rsrc.capitalize()][0]
    def restore_resource(self,rsrc,amount=1):
        return self.name.capitalize() + " gained " + str(amount) + " " + rsrc.capitalize() + """.
Now at""" + self.resources[rsrc.capitalize()][1] + "/" + self.resources[rsrc.capitalize()][0]
    def reset_resource(self,rsrc):
        response = ""
        if rsrc.capitalize() == "All":
            for r in self.resourcelist:
                response += r + " reset from " + str(self.resources[r][0]) + " to " + str(self.resources[r][1]) + "\n"
            self.reset_all_resource()
        elif rsrc.capitalize() == "Buffs":
            response += "Resetting buffs:\n"
            for buff in self.buffs.keys():
                response += self.get_property(buff) + "\n"
            self.reset_buffs()
        else:
            response = "Resetting " + rsrc + " from " + str(self.resources[rsrc.capitalize()][0]) + " to " + str(self.resources[rsrc.capitalize()][1])
            self.resources[rsrc.capitalize()][0] = self.resources[rsrc.capitalize()][1]
        return response
    def reset_all_resource(self):
        for rsrc in self.resources.keys():
                self.resources[rsrc][0] = self.resources[rsrc][1]
    def create_arsenal(self,arsenal):
        arsenal = arsenal.capitalize()
        if len(arsenal)<1:
            return "ERROR: Collection not found in request"
        if arsenal in self.arsenals:
            return "ERROR: Already exists."
        self.arslist.append(arsenal)
        self.arsenals[arsenal] = []
        return "Created successfully."
    def remove_arsenal(self, arsenal):
        arsenal = arsenal.capitalize()
        if len(arsenal)<1:
            return "ERROR: Collection not found in request"
        if arsenal not in self.arsenals:
            return "ERROR: Already exists."
        self.arslist.remove(arsenal)
        del self.arsenals[arsenal.capitalize()]
        return "Deleted successfully"
    def add_item_to_arsenal(self,arsenal,item):
        self.arsenals[arsenal.capitalize()].append(item)
        return "Added."
    def remove_item_from_arsenal(self,arsenal,item):
        self.arsenals[arsenal.capitalize()].remove(item)
        return "Removed."
    def reset_buffs(self):
        response = "Buffs before reset:\n"
        for buff in self.buffs.keys():
            response += self.buffs[buff] + " " + buff + "(base " + self.get_numeric_stat(buff) + ")\n"
        self.buffs = {}
        return response
    def add_buff(self,stat,amount):
        key = ""
        cat = ""
        stat = stat.capitalize()
        for category in self.stats.keys():
            for entry in self.stats[category].keys():
                if entry == stat.capitalize():
                    key = entry
                    cat = category
                    break
            if key != "":
                break
        if key == "":
            for entry in self.resources.keys():
                if entry == stat.capitalize():
                    key = entry
                    cat = "resource"
                    break
        if key == "":
            return "The character lacks this stat or resource.\n*Check spelling or add a new one*."
        self.buffs[stat] = int(amount)
        total = 0
        if cat != "resource":
            total += self.stats[cat][stat]
        else:
            total += self.resources[stat][1]
        total += self.buffs[stat]
        return stat + " buffed to " + str(total) + " for " + self.name + "!"
    
    def get_property(self,prop):
        prop = prop.capitalize()
        if prop == "All" or prop == "Sheet":
            return str(self)
        for description in self.descriptions.keys():
            if description == prop:
                return self.name + "'s " + prop + ": " + self.descriptions[prop] 
        for category in self.stats.keys():
            for stat in self.stats[category].keys():
                if stat == prop:
                    for buff in self.buffs.keys():
                        if buff == prop:
                            return self.name + "'s " + prop + ": " + str(self.stats[category][prop]+self.buffs[prop]) + " (normally " + str(self.stats[category][prop]) + ")" 
                    return self.name + "'s " + prop + ": " + str(self.stats[category][prop])
        for resource in self.resources.keys():
            if resource == prop:
                for buff in self.buffs.keys():
                    if buff == prop:
                        return self.name + "'s " + prop + ": " + str(self.resources[prop][0]) + "/" + str(self.resources[prop][1]+self.buffs[prop]) + " (normally " + str(self.resources[prop][1]) + ")" 
                return self.name + "'s " + prop + ": " + str(self.resources[prop][0]) + "/" + str(self.resources[prop][1])
        for arsenal in self.arsenals.keys():
            if arsenal == prop:
                result = "**" + arsenal + ":** "
                for item in self.arsenals[arsenal]:
                    result += item + ", "
                result = result.strip(', ')
                return result
        return "Could not find " + prop + " for " + self.name
    
    def set_property(self,prop,value):
        prop = prop.capitalize()
        for description in self.descriptions.keys():
            if description == prop:
                self.descriptions[prop] = value
                return "Successfully changed."
        for category in self.stats.keys():
            for stat in self.stats[category].keys():
                if stat == prop:
                    try:
                        self.stats[category][prop] = int(value)
                    except:
                        return "Error: Could not determine number value."
                    return "Successfully changed."
        for resource in self.resources.keys():
            if resource == prop:
                try:
                    self.resources[prop][0] = int(value)
                except:
                    return "Error: Could not determine number value."
                return "Successfully changed."
        for arsenal in self.arsenals.keys():
            if arsenal == prop:
                return "Error: Arsenals can not be 'set'."
        return "Could not find " + prop + " for " + self.name
    
    def delete_property(self,prop):
        prop = prop.capitalize()
        for description in self.descriptions.keys():
            if description == prop:
                self.remove_description(prop)
                return "Successfully deleted."
        for category in self.stats.keys():
            for stat in self.stats[category].keys():
                if stat == prop:
                    try:
                        self.remove_stat(prop)
                    except:
                        return "Error: Could not determine number value."
                    return "Successfully deleted."
        for resource in self.resources.keys():
            if resource == prop:
                try:
                    self.remove_resource(prop)
                except:
                    return "Error: Could not determine number value."
                return "Successfully deleted."
        for arsenal in self.arsenals.keys():
            if arsenal == prop:
                self.remove_arsenal(prop)
                return "Successfully deleted."
        return "Could not find " + prop + " for " + self.name
    
    def rename_property(self,prop,newname):
        prop = prop.capitalize()
        newname = newname.capitalize()
        for description in self.descriptions.keys():
            if description == prop:
                self.descriptions[newname] = self.descriptions[prop]
                del self.descriptions[prop]
                self.desclist[self.desclist.index(prop)] = newname
                return "Successfully changed."
        for category in self.stats.keys():
            for stat in self.stats[category].keys():
                if stat == prop:
                    try:
                        self.stats[category][newname] = self.stats[category][prop]
                        del self.stats[category][prop]
                        cati = self.statlist[0].index(category)+1
                        proi = self.statlist[cati].index(prop)
                        self.statlist[cati][proi] = newname
                    except:
                        return "ERROR: ??? I don't even know what kind, none was predicted to happen."
                    return "Successfully changed."
        for resource in self.resources.keys():
            if resource == prop:
                try:
                    self.resources[newname] = self.resources[prop]
                    del self.resources[prop]
                    self.resourcelist[self.resourcelist.index(prop)] = newname
                except:
                    return "ERROR: ??? I don't even know what kind, none was predicted to happen."
                return "Successfully changed."
        for arsenal in self.arsenals.keys():
            if arsenal == prop:
                self.arsenals[newname] = self.arsenals[prop]
                del self.arsenals[prop]
                self.arslist[self.arslist.index(prop)] = newname
                return "Successfully changed."
        return "Could not find " + prop + " for " + self.name
    
    def template(self,ttype):
        ttype = ttype.capitalize()
        self.add_description("Character Name")
        self.add_description("Nature")
        self.add_description("Demeanor")
        
        self.add_stat_category("Physical")
        self.add_stat("Physical", "Strength")
        self.add_stat("Physical", "Dexterity")
        self.add_stat("Physical", "Stamina")
        
        self.add_stat_category("Social")
        self.add_stat("Social", "Charisma")
        self.add_stat("Social", "Manipulation")
        self.add_stat("Social", "Appearance")
        
        self.add_stat_category("Mental")
        self.add_stat("Mental", "Perception")
        self.add_stat("Mental", "Intelligence")
        self.add_stat("Mental", "Wits")
        self.add_stat_category("Talent")
        self.add_stat_category("Skill")
        self.add_stat_category("Knowledge")
        self.create_resource("Willpower")
        self.create_arsenal("Item")
        self.add_item_to_arsenal("Item", "Clothes")
        if ttype == "Vampire" or ttype == "V20" :
            self.add_health_level(0)
            self.add_health_level(1)
            self.add_health_level(1)
            self.add_health_level(2)
            self.add_health_level(2)
            self.add_health_level(5)
            self.health.sort(key=penalty_sort, reverse=False)
            self.add_description("Clan")
            self.add_description("Generation")
            self.add_stat_category("Discipline")
            self.add_stat("Discipline","Potence")
            self.add_stat("Discipline","Celerity")
            self.add_stat("Discipline","Fortitude")
            self.add_stat_category("Virtue")
            self.add_stat("Virtue","Conscience")
            self.add_stat("Virtue","Self-control")
            self.add_stat("Virtue","Courage")
            self.add_stat_category("Road")
            self.add_stat("Road","Humanity")
            for talent in ["Alertness", "Athletics", "Awareness", "Brawl", "Empathy", "Expression", "Intimidation", "Leadership", "Streetwise", "Subterfuge"]:
                self.add_stat("Talent", talent)
            for skill in ["Animal-Ken", "Crafts", "Drive", "Etiquette", "Firearms", "Larceny", "Melee", "Performance", "Stealth", "Survival"]:
                self.add_stat("Skill", skill)
            for knowledge in ["Academics", "Computer", "Finance", "Investigation", "Law", "Medicine", "Occult", "Politics", "Science", "Technology"]:
                self.add_stat("Knowledge", knowledge)
            self.create_resource("Blood")
            self.set_resource_capacity("Blood", "10")
            self.set_resource("Blood", 10)
            self.create_resource("Blood-per-Turn")
#         elif ttype == "Vda" or ttype == "V:da" or ttype == "V20da":
#             self.descriptions["Clan"] = "Some"
#             self.descriptions["Generation"] = "12th"
#             self.stats["Talent"] = {"Alertness": 0, "Athletics": 0, "Awareness": 0, "Brawl": 0, "Empathy": 0, "Expression": 0, "Intimidation": 0, "Leadership": 0, "Legerdemain": 0, "Subterfuge": 0}
#             self.stats["Skill"] = {"Animal-Ken": 0, "Archery": 0, "Commerce": 0, "Crafts": 0, "Etiquette": 0, "Melee": 0, "Performance": 0, "Ride": 0, "Stealth": 0, "Survival": 0}
#             self.stats["Knowledge"] = {"Academics": 0, "Enigmas": 0, "Hearth Wisdom": 0, "Investigation": 0, "Law": 0, "Medicine": 0, "Occult": 0, "Politics": 0, "Senechal": 0, "Theology": 0}
#             self.resources["Blood"] = [11,11]
#         elif ttype == "Werewolf" or ttype == "Fera" or ttype == "W20" or ttype == "We20":
#             del self.descriptions["Nature"] #Fera have neither Nature nor Demeanor for some reason
#             del self.descriptions["Demeanor"]
#             self.descriptions["Tribe"] = "Tribalistic"
#             self.descriptions["Auspice"] = "Auspicious"
#             self.descriptions["Breed"] = "One of three, I bet"
#             self.stats["Talent"] = {"Alertness": 0, "Athletics": 0, "Brawl": 0, "Empathy": 0, "Expression": 0, "Leadership": 0, "Intimidation": 0, "Primal-Urge": 0, "Streetwise": 0, "Subterfuge": 0}
#             self.stats["Skill"] = {"Animal-Ken": 0, "Crafts": 0, "Drive": 0, "Etiquette": 0, "Firearms": 0, "Larceny": 0, "Melee": 0, "Performance": 0, "Stealth": 0, "Survival": 0}
#             self.stats["Knowledge"] = {"Academics": 0, "Computer": 0, "Enigmas": 0, "Investigation": 0, "Law": 0, "Medicine": 0, "Occult": 0, "Rituals": 0, "Science": 0, "Technology": 0}
#             self.resources["Rage"] = [1,1]
#             self.resources["Gnosis"] = [1,1]
#             self.resources["Glory"] = [1,1]
#             self.resources["Honor"] = [1,1]
#             self.resources["Wisdom"] = [1,1]
#         elif ttype == "Mage" or ttype == "M20":
#             self.stats["Spheres"] = {"Arete": 0,"Correspondence": 0,"Entropy": 0,"Forces": 0,"Life": 0,"Matter": 0,"Mind": 0,"Prime": 0,"Spirit": 0,"Time": 0}
#             self.stats["Talent"] = {"Alertness": 0, "Art": 0, "Athletics": 0, "Awareness": 0, "Brawl": 0, "Empathy": 0, "Expression": 0, "Intimidation": 0, "Leadership": 0, "Streetwise": 0, "Subterfuge": 0}
#             self.stats["Skill"] = {"Crafts": 0, "Drive": 0, "Etiquette": 0, "Firearms": 0, "Martial Arts": 0, "Meditation": 0, "Melee": 0, "Research": 0, "Stealth": 0, "Survival": 0, "Technology": 0}
#             self.stats["Knowledge"] = {"Academics": 0, "Computer": 0, "Cosmology": 0, "Enigmas": 0, "Esoterica": 0, "Investigation": 0, "Law": 0, "Medicine": 0, "Occult": 0, "Politics": 0, "Science": 0}
#             self.resources["Quintessence"] = [10,10]
#             self.resources["Paradox"] = [0,10]
#         elif ttype == "Changeling" or ttype == "C20":
#             return "Changeling templates are not yet supported."
#         elif ttype == "Wraith" or ttype == "Wr20":
#             return "Wraith templates are not yet supported."
#         elif ttype == "Demon":
#             return "Demon templates are not yet supported"
#         elif ttype == "Spirit":
#             self.stats = {}
#             self.resources["Rage"] = [1,1]
#             self.resources["Gnosis"] = [1,1]
#             self.resources["Essence"] = [1,1]
#         elif ttype == "Human":
#             pass
             
        
    def initialize_from_string(self, text):
        section = text.split("\n---\n")
        try:
            identifiers = section[0].splitlines()
            descriptions = section[1].splitlines()
            stats = section[2].splitlines()
            resources = section[3].splitlines()
            arsenals = section[4].splitlines()
            self.name = identifiers[0].split(' ')[1]
            self.owner = identifiers[1].split(' ')[1]
            self.st = identifiers[2].split(' ')[1]
            h = identifiers[3].partition(' \t')[2]
            for level in h.split(','):
                self.health.append(int(level))
            d = identifiers[4].partition(' \t\t')[2]
            for level in d.split(','):
                self.damage.append(level)
            self.health.sort(key=penalty_sort, reverse=False)
            self.damage.sort(key=damage_sort, reverse=False)
            for line in descriptions:
                linepts = line.partition(':** ')
                self.add_description(linepts[0].strip(' *:_'))
                self.set_description(linepts[0].strip(' *:_'), linepts[2])
            for i in range(0,len(stats),2):
                self.add_stat_category(stats[i].strip(' *:_'))
                for element in stats[i+1].strip('\t').split('\t'):
                    self.add_stat(stats[i].strip(' *:_'), element.split(':** ')[0].strip(' *:_'))
                    self.set_stat(element.split(' ')[0].strip(' *:_'), int(element.split(' ')[1]))
            for line in resources:
                linepts = line.partition(':** ')
                self.create_resource(linepts[0].strip(' *:_'))
                self.set_resource_capacity(linepts[0].strip(' *:_'), int(linepts[2].split('/')[1]))
                self.set_resource(linepts[0].strip(' *:_'), int(linepts[2].split('/')[0]))
            for line in arsenals:
                linepts = line.partition(':** ')
                self.create_arsenal(linepts[0].strip(' *:_'))
                for element in linepts[2].split(', '):
                    self.add_item_to_arsenal(linepts[0].strip(' *:_'), element)
        except Exception as e:
            return "Unable to read sheet: " + str(e)
        return False

# Short test!
# bob = WoDCharacter("bob","J")
# bob.template("Vampire")
# print(bob)
# print("End of Generated Bob")
# bobfile = open("sheets/bob.txt","w")
# bobfile.write(str(bob))
# bobfile.close()
# bobfile = open("sheets/bob.txt","r")
# bob = WoDCharacter(bobfile.read())
# print(bob.display())
# bobfile.close()
# print(bob.health)





