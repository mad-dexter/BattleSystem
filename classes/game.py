import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.name = name
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Inventory"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_maxmp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def heal_hp(self, heal_points):
        self.hp += heal_points
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def heal_mp(self, heal_points):
        self.mp += heal_points
        if self.mp > self.max_mp:
            self.mp = self.max_mp

    def choose_action(self):
        i = 1
        print(self.name)
        print("ACTIONS")
        for act in self.actions:
            print("    ", str(i), ": ", act)
            i += 1

    def choose_spell(self):
        i = 1
        print("MAGICS")
        for mag in self.magic:
            print("    ", str(i), ". ", mag.name, ": Cost - ", mag.cost)
            i += 1
        print("    ", "0. To go back to main menu")

    def choose_inventory_items(self):
        i = 1
        print("ITEMS")
        for item in self.items:
            print("    ",str(i), ".", item["item"].name, ": ", item["item"].description, "  (x" + str(item["quantity"]) + ")")
            i += 1
        print("    ", "0. To go back to main menu")

    def get_enemy_status(self):
        hp_bar = ""
        mp_bar = ""
        checked_count = (self.hp / self.max_hp) * 100 / 2
        while checked_count > 0:
            hp_bar += '█'
            checked_count -= 1
        # Fill the white space for the left out area in HP
        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.max_hp)
        current_hp_string = ""
        # Code to check if the HP falls below 7 digits. In such case realign the bars.
        if len(hp_string) < 9:
            hp_length_les_count = 9 - len(hp_string)
            while hp_length_les_count > 0:
                current_hp_string += " "
                hp_length_les_count -= 1
            current_hp_string += hp_string
        else:
            current_hp_string = hp_string

        mp_string = str(self.mp) + "/" + str(self.max_mp)
        current_mp_string = ""
        # Code to check if the MP falls below 5 digit. In such case realign the bars
        if len(mp_string) < 9:
            mp_length_less_count = 9 - len(mp_string)
            while mp_length_less_count > 0:
                mp_length_less_count -= 1
                current_mp_string += " "
            current_mp_string += mp_string
        else:
            current_mp_string = mp_string

        print(bcolors.BOLD + self.name + "        " + current_hp_string + "|" + bcolors.FAIL + hp_bar
              + bcolors.ENDC + "|")
        print("\n\n")

    def get_player_status(self):
        hp_bar = ""
        mp_bar = ""
        checked_count = (self.hp/self.max_hp)*100/4
        while checked_count > 0:
            hp_bar += '█'
            checked_count -= 1
        # Fill the white space for the left out area in HP
        while len(hp_bar) < 25:
            hp_bar += " "

        checked_mp_count = (self.mp/self.max_mp)*100/10
        # Fill the white space for the left out area in HP
        while checked_mp_count > 0:
            mp_bar += '█'
            checked_mp_count -= 1
        while len(mp_bar) < 10:
            mp_bar += " "


        hp_string = str(self.hp)+"/"+str(self.max_hp)
        current_hp_string = ""
        # Code to check if the HP falls below 7 digits. In such case realign the bars.
        if len(hp_string) < 7:
            hp_length_les_count = 7 - len(hp_string)
            while hp_length_les_count > 0:
                current_hp_string += " "
                hp_length_les_count -= 1
            current_hp_string += hp_string
        else:
            current_hp_string = hp_string

        mp_string = str(self.mp)+"/"+str(self.max_mp)
        current_mp_string = ""
        # Code to check if the MP falls below 5 digit. In such case realign the bars
        if len(mp_string) < 5:
            mp_length_less_count = 5 - len(mp_string)
            while mp_length_less_count > 0:
                mp_length_less_count -= 1
                current_mp_string += " "
            current_mp_string += mp_string
        else:
            current_mp_string = mp_string

        print(bcolors.BOLD + self.name +"            "+current_hp_string+"|" + bcolors.OKGREEN + hp_bar
              + bcolors.ENDC + "|      "+bcolors.BOLD + current_mp_string + "|" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")
        print("\n\n")

    def generate_magic_spell(self):
        magic_choose = True
        temp_magic = self.magic
        magic_index = -1
        # if less HP, the only choose white magic
        if self.get_hp() < 100:
            magic_index = 0
            for mag in self.magic:
                if mag.type == "white":
                    if mag.cost <= self.get_mp():
                        return magic_index
                    else:
                        return -2
                magic_index += 1
        while magic_choose:
            if len(temp_magic) == 0:
                magic_choose = False
                continue
            magic_index = random.randrange(0, len(temp_magic))
            magic_cost = temp_magic[magic_index].get_spell_cost()
            # Check if the guy has the adequate cost to cast the spell
            if self.get_mp() >= magic_cost:
                # Player can cast the spell. So return the index
                magic_choose = False
            else:
                del temp_magic[magic_index]
                magic_index = -1
                continue

        return magic_index
