from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import classes.battleconstants as constant
import random
import json

# Items objects Instantiation
playerlevel = 1
playerpoints = 0
# Black magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 12, 130, "black")
blizzard = Spell("Blizzard", 14, 140, "black")
quake = Spell("EarthQuake", 18, 250, "black")
meteor = Spell("Meteor", 16, 200, "black")

# White magic
cure = Spell("Cure", 10, 120, "white")
cura = Spell("Cura", 24, 200, "white")
curion = Spell("Curion", 30, 300, "white")

# Inventory Items instantiation
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super-Potion", "potion", "Heals 500 HP", 500)
exilir = Item("Exilir", "exilir", "Fully restores HP/MP of one Party's member", 9999)
hiexilir = Item("Hi-Elixlir", "exilir", "Fully restores HP/MP for the party", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

# End of Items instantiation
# Check if player wants to load old progress of start a new game
player_game_input = 0
stats_json = {}


def game_selection():
    global player_game_input, playerlevel, playerpoints, stats_json
    print(bcolors.BOLD + "Game Selection:" + bcolors.ENDC)
    print("    1. Start new Game")
    print("    2. Load from last saved")
    print("    3. Check player Stats")
    player_game_input = int(input("Make a choice to start: "))
    stat_file = open("./jsondata/playerstats.json", "r+")
    stats_json = json.loads(stat_file.read())
    if player_game_input is 1:
        # Reset all the stats to start a new game
        stats_json["playerlevel"] = 1
        stats_json["playerpoints"] = 0
        playerlevel = 1
        playerpoints = 0
        stat_file.seek(0)
        stat_file.write(json.dumps(stats_json))
    elif player_game_input is 2:
        playerlevel = stats_json["playerlevel"]
        playerpoints = stats_json["playerpoints"]
    elif player_game_input is 3:
        playerlevel = stats_json["playerlevel"]
        playerpoints = stats_json["playerpoints"]
        print("    " + bcolors.BOLD + bcolors.WARNING + "Your current level is : " + str(playerlevel) +
              " and " + str(
            constant.MAX_LEVEL_POINTS - playerpoints) + " points to reach the next level." + bcolors.ENDC)
        stat_file.close()
        game_selection()
    stat_file.close()


game_selection()

player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 1},
                {"item": exilir, "quantity": 2},
                {"item": hiexilir, "quantity": 1},
                {"item": grenade, "quantity": 5}]

# Initialize the players
selected_player = []
players = []
player_file = open("./jsondata/autobots.json", "r")
player_list = json.loads(player_file.read())
i = 0
print("Choose your characters: ")
for pplayer in player_list["playerlist"]:
    i += 1
    print("    ", str(i), ". ", pplayer["name"], ", HP : ", pplayer["hp"])

for j in range(3):
    playerinp = int(input("Select a character : ")) - 1
    selected_player.append(playerinp)

# once we got the players selected create the players object
player_magic = []
for index in selected_player:
    player_magic = []
    for magic in player_list["playerlist"][index]["magic"]:
        if magic == "fire":
            player_magic.append(fire)
        elif magic == "thunder":
            player_magic.append(thunder)
        elif magic == "blizzard":
            player_magic.append(blizzard)
        elif magic == "quake":
            player_magic.append(quake)
        elif magic == "meteor":
            player_magic.append(meteor)
        elif magic == "cure":
            player_magic.append(cure)
        elif magic == "cura":
            player_magic.append(cura)
        elif magic == "curion":
            player_magic.append(curion)
    player = player_list["playerlist"][index]
    players.append(
        Person(player["name"], player["hp"], player["mp"], player["atk"], player["def"], player_magic, player_items))

player_file.close()
# Initialize the enemies
enemies = []
enemy_magic = []
enemy_file = open("./jsondata/decepticons.json", "r")
enemy_json = json.loads(enemy_file.read())
for enemy in enemy_json["enemies"]:
    if enemy["level"] == playerlevel:
        enemy_magic = []
        for magic in enemy["magic"]:
            if magic == "fire":
                enemy_magic.append(fire)
            elif magic == "thunder":
                enemy_magic.append(thunder)
            elif magic == "blizzard":
                enemy_magic.append(blizzard)
            elif magic == "quake":
                enemy_magic.append(quake)
            elif magic == "meteor":
                enemy_magic.append(meteor)
            elif magic == "cure":
                enemy_magic.append(cure)
            elif magic == "cura":
                enemy_magic.append(cura)
            elif magic == "curion":
                enemy_magic.append(curion)
        enmy = Person(enemy["name"], enemy["hp"], enemy["mp"], enemy["atk"], enemy["def"], enemy_magic, [])
        enemies.append(enmy)

enemy_file.close()


# Method to show the list of enemies to attack
def choose_enemy_to_attack():
    i = 1
    print("ENEMIES")
    for enemy in enemies:
        print(str(i) + ". " + enemy.name)
        i += 1


# Method to delete items from array
def delete_items_from_list(array, index):
    del array[index]
    return array


# Method to set the player level and points
def set_player_level_and_points(winorloss):
    global playerpoints
    global playerlevel
    if winorloss == "loss":
        if playerpoints > constant.LOSING_POINTS:
            playerpoints -= constant.LOSING_POINTS
        else:
            playerpoints = 0
    else:
        if playerlevel is not constant.MAX_LEVEL:
            # With this condition player cannot go beyond the max level
            playerpoints += constant.WINNING_POINTS
            if playerpoints >= constant.MAX_LEVEL_POINTS:
                # increase the player level
                playerlevel += 1
                playerpoints = 0


running = True

print(bcolors.FAIL + bcolors.BOLD + "The Enemy Attacks" + bcolors.ENDC)
can_enemy_atk_back = True
while running:
    # Show player stats at the beginning
    print("\n")
    print(
        bcolors.BOLD + bcolors.UNDERLINE + "NAME                           HP                                     MP" + bcolors.ENDC)
    for player in players:
        player.get_player_status()
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_status()

    print(bcolors.BOLD + "Your Level : " + str(playerlevel) + bcolors.ENDC)

    # Start the actual attack process
    for player in players:
        print("=====================================")
        choose_enemy_to_attack()
        atk_choice = int(input("Select an enemy to attack: ")) - 1

        player.choose_action()
        act_choice = input("Enter your choice of actions : ")
        index = int(act_choice) - 1

        # If the choice is to Attack
        if index == 0:
            damage = player.generate_damage()
            enemies[atk_choice].take_damage(damage)
            print("You have attacked " + enemies[atk_choice].name + " for " + str(damage) + " damage points.")

        # If choice is to cast a magic
        elif index == 1:
            player.choose_spell()
            spell_choice = int(input("Select a Magic :")) - 1

            # Check if the player selected to go back
            if spell_choice == -1:
                continue

            spell = player.magic[spell_choice]
            magic_dmg = spell.generate_spell_damage()
            cost = spell.get_spell_cost()

            # Check if the player has enough MP to cast the spell
            if cost > player.get_mp():
                print(bcolors.FAIL + "You don't have enough Magic points to cast the spell" + bcolors.ENDC)
                continue

            # The player wants to heal
            if spell.type == "white":
                player.heal_hp(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals the player by " + str(
                    magic_dmg) + " points" + bcolors.ENDC)
            elif spell.type == "black":
                enemies[atk_choice].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(
                    magic_dmg) + " points of damage to " + enemies[atk_choice].name + bcolors.ENDC)

            player.reduce_mp(cost)

        else:
            player.choose_inventory_items()
            item_choice = int(input("Choose an Item :")) - 1

            # Check if the player selected to go back
            if item_choice == -1:
                continue

            itm = player.items[item_choice]["item"]
            itm_quantity = player.items[item_choice]["quantity"]
            item_dmg = itm.prop

            # Check if the player has adequate item quantity
            if itm_quantity > 0:
                # Check what kind of item the player has selected
                if itm.type == "attack":
                    enemies[atk_choice].take_damage(item_dmg)
                    print(
                        bcolors.OKBLUE + "\n" + itm.name + " dealt " + str(item_dmg) + " to the " + enemies[
                            atk_choice].name + "." + bcolors.ENDC)
                elif itm.type == "potion":
                    player.heal_hp(item_dmg)
                    print(bcolors.OKGREEN + "\n" + itm.name + " heals the player by " + str(
                        item_dmg) + " points" + bcolors.ENDC)
                elif itm.type == "exilir":
                    if itm.name == "Exilir":
                        player.hp = player.max_hp
                        player.mp = player.max_mp
                        print("The player HP/MP has been restored fully")
                    elif itm.name == "Hi-Elixlir":
                        # Restore health of all the players in the party
                        for p in players:
                            p.hp = p.max_hp
                            p.mp = p.max_mp
                        print("All the players HP/MP has been restored successfully")

                # Reduce the quantity of the item after applied successfully
                player.items[item_choice]["quantity"] -= 1
            else:
                # Player does not have adequate quantity. Show error
                print(bcolors.FAIL + "Your don't have enough quantity of the selected item." + bcolors.ENDC)
                continue

        # Check if the enemy is dead after an attack
        if enemies[atk_choice].get_hp() == 0:
            print(bcolors.FAIL + enemies[atk_choice].name + " has died." + bcolors.ENDC)
            # once the enemy is dead remove it from the array
            delete_items_from_list(enemies, atk_choice)
            # Check if any enemies are left
            if len(enemies) == 0:
                can_enemy_atk_back = False
                break

    if not can_enemy_atk_back:
        # All the enemies died and they can no more attack
        print(bcolors.OKGREEN + "You Won!!!" + bcolors.ENDC)
        set_player_level_and_points("win")
        running = False
        stats_json["playerlevel"] = playerlevel
        stats_json["playerpoints"] = playerpoints
        stat_file = open("./jsondata/playerstats.json", "r+")
        stat_file.write(json.dumps(stats_json))
        stat_file.close()
    else:

        # Also enemy will cast a damage when attack. If only the enemy is alive
        is_any_enemy_alive = False
        for enemy in enemies:
            if enemy.get_hp() > 0:
                is_any_enemy_alive = True
                break

        # Also select randomly which enemy will generate the damage
        if len(enemies) > 1:
            random_enemy_index = random.randrange(0, len(enemies))
        else:
            random_enemy_index = 0

        if is_any_enemy_alive:
            if enemies[random_enemy_index].get_hp() < 100:
                # Enemy will automatically use white magic
                enemy_action = 1
            else:
                enemy_action = random.randrange(0, 2)
            enemy_dmg = 0
            # Beginning of block to incur damage on players
            if enemy_action == 0:
                enemy_action_name = "Attack"
                # Enemy attacks
                enemy_dmg = enemies[random_enemy_index].generate_damage()
            elif enemy_action == 1:
                # Enemy uses magic
                # Generate which magic to choose
                enemy_magic_index = enemies[random_enemy_index].generate_magic_spell()
                if enemy_magic_index > -1:
                    enemy_spell = enemies[random_enemy_index].magic[enemy_magic_index]
                    if enemy_spell.type == "white":
                        enemies[random_enemy_index].heal_hp(enemy_spell.dmg)
                        print(
                            enemies[random_enemy_index].name + " healed itself by " + str(enemy_spell.dmg) + " points.")
                    else:
                        enemy_dmg = enemy_spell.generate_spell_damage()
                        enemy_magic_cost = enemy_spell.get_spell_cost()
                        enemies[random_enemy_index].reduce_mp(enemy_magic_cost)
                    enemy_action_name = "Magic"
                elif enemy_magic_index == -2:
                    # No more MP left in enemy for heal. So attack the player
                    enemy_dmg = enemies[random_enemy_index].generate_damage()
                    enemy_action_name = "Magic"
            # End of code block.

            # Generate a random player to take damage from player list
            if len(players) > 1:
                player_for_dmg = random.randrange(0, len(players))
            else:
                player_for_dmg = 0
            players[player_for_dmg].take_damage(enemy_dmg)
            print(bcolors.FAIL + enemies[random_enemy_index].name + " attacked back player: " + players[
                player_for_dmg].name + " with " + enemy_action_name
                  + ": " + str(enemy_dmg) + " damage points." + bcolors.ENDC)

        # Check if the player who was attacked has died
        is_any_player_alive = False
        if players[player_for_dmg].hp == 0:
            print(bcolors.FAIL + "Player " + players[player_for_dmg].name + " has died." + bcolors.ENDC)
            players = delete_items_from_list(players, player_for_dmg)
        # Check if any player is alive
        for player in players:
            if player.get_hp() > 0:
                is_any_player_alive = True
                break

        # Check if anyone has won
        if not is_any_player_alive:
            print(bcolors.FAIL + "You have been defeated !!! Try again" + bcolors.ENDC)
            set_player_level_and_points("loss")
            running = False
        elif not is_any_enemy_alive:
            print(bcolors.OKGREEN + "You Won!!!" + bcolors.ENDC)
            set_player_level_and_points("win")
            running = False
        stats_json["playerlevel"] = playerlevel
        stats_json["playerpoints"] = playerpoints
        stat_file = open("./jsondata/playerstats.json", "r+")
        stat_file.write(json.dumps(stats_json))
        stat_file.close()
