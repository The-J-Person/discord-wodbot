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

class WoDCharacter:
    def __init__(self, text=None, owner=None):
        self.name = text
        self.owner = owner
        self.st = None
        self.descriptions = {}
        self.stats = {}
        self.buffs = {}
        self.resources = {}
        self.arsenals = {}
        if text!=None and owner==None:
            self.initialize_from_string(text)
    def __str__(self,):
        return "---\n".join(self.to_text_section(0))
    def to_text_section(self,limit=2000): #Discord Message Length Limit is 2000. This is now addressed in another file.
        # Thus, this function's features serve no purpose.
        section = []
        result = "**Name:** " + self.name + "\n**Owner:** " + self.owner +"\n**Storyteller**: " + str(self.st) + "\n"
        section.append(result)#result += "---\n"
        result = ""
        for description in sorted(self.descriptions.keys(), key=lambda k: sortkey(k)):
            ###
            # WARNING! Not checking if a single description is over-limit!
            # If someone writes a single description of over 2000 characters, this part will lock up.
            ###
            if limit>0 and len(result)+len("**" + description + ":** " + self.descriptions[description] + "\n")>limit:
                section.append(result)#result += "---\n"
                result = ""
            result += "**" + description + ":** " + self.descriptions[description] + "\n"
        section.append(result)#result += "---\n"
        result = ""
        for category in sorted(self.stats.keys(), key=lambda k: sortkey(k)):
            ###
            # WARNING! The stats section is not being checked for being over-limit!
            # Note to self: Add such a check later...
            ###
            result += "__**" + category + ":**__\n"
            for stat in self.stats[category].keys():
                result += "**" + stat + ":** " + str(self.stats[category][stat]) + "\t"
            result += "\n"
        section.append(result)#result += "---\n"
        result = ""
        for resource in sorted(self.resources.keys(), key=lambda k: sortkey(k)):
            ###
            # WARNING! The resources section is not being checked for being over-limit!
            # Albeit unlikely, a check should be added.
            ###
            result += "**" + resource + ":** " + str(self.resources[resource][0]) + "/" + str(self.resources[resource][1]) + "\n"
        section.append(result)#result += "---\n"
        result = ""
        for bag in self.arsenals.keys():
            ###
            # WARNING! The arsenals section is not being checked for being over-limit!
            # Note to self: Add such a check later...
            ###
            result += "**" + bag + "**: "
            for item in self.arsenals[bag]:
                result += item + ", "
            result = result.strip(', ')
            result+="\n"
        result = result.strip('\n')
        section.append(result)
        return section
    def set_name(self,name):
        self.name = name
    def set_owner(self,owner):
        self.owner = owner
    def set_st(self,st):
        self.st = st
    def remove_description(self,desc):
        del self.descriptions[desc]
    def set_description(self,desc,content):
        self.descriptions[desc.capitalize()] = content
        return desc.capitalize() + " set for " + self.name + "!"
    def add_stat_category(self,cat_name):
        if cat_name.capitalize() in self.stats:
            return "Already exists."
        self.stats[cat_name.capitalize()] = {}
        return "Created successfully."
    def add_stat(self, category, name):
        if category.capitalize() not in self.stats:
            return "You don't have such a stat category."
        if name.capitalize() in self.stats[category]:
            return "This stat already exists."
        self.stats[category.capitalize()][name.capitalize()] = 0
        return "Created successfully."
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
        return stat.capitalize() + " set to " + level + " for " + self.name + "!"
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
    def create_resource(self,rsrc):
        self.resources[rsrc.capitalize()] = [1,1]
    def remove_resource(self,rsrc):
        del self.resources[rsrc.capitalize()]
    def set_resource(self,rsrc,amount):
        self.resources[rsrc.capitalize()][0] = int(amount)    
        return rsrc + " set to " + amount + "/" + str(self.resources[rsrc][1]) + " for " + self.name + "!"
    def set_resource_capacity(self,rsrc,amount):
        self.resources[rsrc.capitalize()][1] = int(amount)
    def consume_resource(self,rsrc,amount=1):
        self.resources[rsrc.capitalize()][0] -= int(amount)
    def restore_resource(self,rsrc,amount=1):
        self.resources[rsrc.capitalize()][0] += int(amount)
    def reset_resource(self,rsrc):
        if rsrc.capitalize() == "All":
            self.reset_all_resource()
        elif rsrc.capitalize() == "Buffs":
            self.reset_buffs()
        else:
            self.resources[rsrc.capitalize()][0] = self.resources[rsrc.capitalize()][1]
    def reset_all_resource(self):
        for rsrc in self.resources.keys():
                self.resources[rsrc][0] = self.resources[rsrc][1]
    def create_arsenal(self,arsenal):
        if arsenal.capitalize() in self.arsenals:
            return "Already exists."
        self.arsenals[arsenal.capitalize()] = []
        return "Created successfully."
    def remove_arsenal(self, arsenal):
        del self.arsenals[arsenal.capitalize()]
    def add_item_to_arsenal(self,arsenal,item):
        self.arsenals[arsenal.capitalize()].append(item)
    def remove_item_from_arsenal(self,arsenal,item):
        self.arsenals[arsenal.capitalize()].remove(item)
    def reset_buffs(self):
        self.buffs = {}
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
                return self.arsenals[prop]
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
    
    def template(self,ttype):
        ttype = ttype.capitalize()
        self.descriptions["Nature"] = "Not picked"
        self.descriptions["Demeanor"] = "Not picked"
        self.descriptions["Description"] = "Not described yet"
        self.stats["Physical"] = {"Strength": 1, "Dexterity": 1, "Stamina": 1}
        self.stats["Social"] = {"Charisma": 1, "Manipulation": 1, "Appearance": 1}
        self.stats["Mental"] = {"Perception": 1, "Intelligence": 1, "Wits": 1}
#         self.stats["Talent"] = {}
#         self.stats["Skill"] = {}
#         self.stats["Knowledge"] = {}
        self.resources["Willpower"] = [1,1]
        self.arsenals["Item"] = ["Clothes","Crumpet"]
        if ttype == "Vampire" or ttype == "V20" :
            self.descriptions["Clan"] = "Some"
            self.descriptions["Generation"] = "13th"
            self.stats["Discipline"] = {"Potence": 0, "Celerity": 0, "Fortitude": 0}
            self.stats["Virtue"] = {"Conscience": 1, "Self-control": 1, "Courage": 1}
            self.stats["Road"] = {"Humanity": 7}
            self.stats["Talent"] = {"Alertness": 0, "Athletics": 0, "Awareness": 0, "Brawl": 0, "Empathy": 0, "Expression": 0, "Intimidation": 0, "Leadership": 0, "Streetwise": 0, "Subterfuge": 0}
            self.stats["Skill"] = {"Animal-Ken": 0, "Crafts": 0, "Drive": 0, "Etiquette": 0, "Firearms": 0, "Larceny": 0, "Melee": 0, "Performance": 0, "Stealth": 0, "Survival": 0}
            self.stats["Knowledge"] = {"Academics": 0, "Computer": 0, "Finance": 0, "Investigation": 0, "Law": 0, "Medicine": 0, "Occult": 0, "Politics": 0, "Science": 0, "Technology": 0}
            self.resources["Blood"] = [10,10]
        elif ttype == "Vda" or ttype == "V:da" or ttype == "V20da":
            self.descriptions["Clan"] = "Some"
            self.descriptions["Generation"] = "12th"
            self.stats["Talent"] = {"Alertness": 0, "Athletics": 0, "Awareness": 0, "Brawl": 0, "Empathy": 0, "Expression": 0, "Intimidation": 0, "Leadership": 0, "Streetwise": 0, "Subterfuge": 0}
            self.stats["Skill"] = {"Animal-Ken": 0, "Crafts": 0, "Drive": 0, "Etiquette": 0, "Firearms": 0, "Larceny": 0, "Melee": 0, "Performance": 0, "Stealth": 0, "Survival": 0}
            self.stats["Knowledge"] = {"Academics": 0, "Computer": 0, "Finance": 0, "Investigation": 0, "Law": 0, "Medicine": 0, "Occult": 0, "Politics": 0, "Science": 0, "Technology": 0}
            self.resources["Blood"] = [11,11]
        elif ttype == "Werewolf" or ttype == "Fera" or ttype == "W20" or ttype == "We20":
            del self.descriptions["Nature"] #Fera have neither Nature nor Demeanor for some reason
            del self.descriptions["Demeanor"]
            self.descriptions["Tribe"] = "Tribalistic"
            self.descriptions["Auspice"] = "Auspicious"
            self.descriptions["Breed"] = "One of three, I bet"
            self.stats["Talent"] = {"Alertness": 0, "Athletics": 0, "Brawl": 0, "Empathy": 0, "Expression": 0, "Leadership": 0, "Intimidation": 0, "Primal-Urge": 0, "Streetwise": 0, "Subterfuge": 0}
            self.stats["Skill"] = {"Animal-Ken": 0, "Crafts": 0, "Drive": 0, "Etiquette": 0, "Firearms": 0, "Larceny": 0, "Melee": 0, "Performance": 0, "Stealth": 0, "Survival": 0}
            self.stats["Knowledge"] = {"Academics": 0, "Computer": 0, "Enigmas": 0, "Investigation": 0, "Law": 0, "Medicine": 0, "Occult": 0, "Rituals": 0, "Science": 0, "Technology": 0}
            self.resources["Rage"] = [1,1]
            self.resources["Gnosis"] = [1,1]
            self.resources["Glory"] = [1,1]
            self.resources["Honor"] = [1,1]
            self.resources["Wisdom"] = [1,1]
        elif ttype == "Mage" or ttype == "M20":
            self.stats["Spheres"] = {"Arete": 0,"Correspondence": 0,"Entropy": 0,"Forces": 0,"Life": 0,"Matter": 0,"Mind": 0,"Prime": 0,"Spirit": 0,"Time": 0}
            self.stats["Talent"] = {"Alertness": 0, "Art": 0, "Athletics": 0, "Awareness": 0, "Brawl": 0, "Empathy": 0, "Expression": 0, "Intimidation": 0, "Leadership": 0, "Streetwise": 0, "Subterfuge": 0}
            self.stats["Skill"] = {"Crafts": 0, "Drive": 0, "Etiquette": 0, "Firearms": 0, "Martial Arts": 0, "Meditation": 0, "Melee": 0, "Research": 0, "Stealth": 0, "Survival": 0, "Technology": 0}
            self.stats["Knowledge"] = {"Academics": 0, "Computer": 0, "Cosmology": 0, "Enigmas": 0, "Esoterica": 0, "Investigation": 0, "Law": 0, "Medicine": 0, "Occult": 0, "Politics": 0, "Science": 0}
            self.resources["Quintessence"] = [10,10]
            self.resources["Paradox"] = [0,10]
        elif ttype == "Changeling" or ttype == "C20":
            return "Changeling templates are not yet supported."
        elif ttype == "Wraith" or ttype == "Wr20":
            return "Wraith templates are not yet supported."
        elif ttype == "Demon":
            return "Demon templates are not yet supported"
        elif ttype == "Spirit":
            self.stats = {}
            self.resources["Rage"] = [1,1]
            self.resources["Gnosis"] = [1,1]
            self.resources["Essence"] = [1,1]
        elif ttype == "Human":
            pass
             
        
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
            for line in descriptions:
                linepts = line.partition(' ')
                self.descriptions[linepts[0].strip(' *:_')] = linepts[2]
            for i in range(0,len(stats),2):
                self.stats[stats[i].strip(' *:_')] = {}
                for element in stats[i+1].strip('\t').split('\t'):
                    self.stats[stats[i].strip(' *:_')][element.split(' ')[0].strip(' *:_')] = int(element.split(' ')[1])
            for line in resources:
                linepts = line.partition(' ')
                self.resources[linepts[0].strip(' *:_')] = [int(linepts[2].split('/')[0]),int(linepts[2].split('/')[1])]
            for line in arsenals:
                linepts = line.partition(' ')
                self.arsenals[linepts[0].strip(' *:_')] = []
                for element in linepts[2].split(', '):
                    self.arsenals[linepts[0].strip(' *:_')].append(element)
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
# print(bob)
# bobfile.close()




