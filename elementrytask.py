import sys
from typing import List, Dict, Callable

# Character class for storing player stats and inventory
class Character:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.health = 100
        self.inventory = []

    def add_item(self, item: str):
        self.inventory.append(item)

    def __str__(self):
        return (f"Name: {self.name}\nRole: {self.role}\nHealth: {self.health}\n"
                f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")

# Game state class for modularity
class GameState:
    def __init__(self):
        self.character = None
        self.story_position = "start"

    def update_position(self, position: str):
        self.story_position = position

# Define a dictionary for branching story paths
story_paths: Dict[str, Callable[[GameState], None]] = {}

# Utility functions

def create_character() -> Character:
    print("Welcome to the adventure!")
    name = input("Enter your character's name: ")
    print("Choose your role:")
    print("1. Warrior\n2. Mage\n3. Rogue")
    role_choice = input("Enter the number of your choice: ")
    roles = {"1": "Warrior", "2": "Mage", "3": "Rogue"}
    role = roles.get(role_choice, "Adventurer")
    print(f"Character created: {name}, the {role}")
    return Character(name, role)

def display_status(character: Character):
    print("\nYour current status:")
    print(character)
    print()

# Story path functions

def start_story(game_state: GameState):
    print("You find yourself at the entrance to a dark forest. What will you do?")
    print("1. Enter the forest\n2. Turn back\n3. Look around")
    choice = input("Enter your choice: ")

    if choice == "1":
        print("You bravely step into the forest.")
        game_state.update_position("forest")
    elif choice == "2":
        print("You decide it's safer to leave. Maybe another day.")
        sys.exit()
    elif choice == "3":
        print("You find a rusty sword on the ground and pick it up.")
        game_state.character.add_item("Rusty Sword")
        game_state.update_position("start")
    else:
        print("Invalid choice, try again.")
        start_story(game_state)

story_paths["start"] = start_story

def forest_story(game_state: GameState):
    print("The forest is dark and full of strange noises. A wild goblin appears!")
    print("1. Fight the goblin\n2. Run away\n3. Try to talk to it")
    choice = input("Enter your choice: ")

    if choice == "1":
        if "Rusty Sword" in game_state.character.inventory:
            print("You defeat the goblin with your rusty sword!")
            game_state.character.add_item("Goblin Loot")
            game_state.update_position("clearing")
        else:
            print("You have no weapon and are defeated. Game over.")
            sys.exit()
    elif choice == "2":
        print("You run back to the start of the forest.")
        game_state.update_position("start")
    elif choice == "3":
        print("The goblin growls and attacks you. You lose health but escape.")
        game_state.character.health -= 20
        game_state.update_position("start")
    else:
        print("Invalid choice, try again.")
        forest_story(game_state)

story_paths["forest"] = forest_story

def clearing_story(game_state: GameState):
    print("You find a peaceful clearing with a mysterious chest.")
    print("1. Open the chest\n2. Rest for a while\n3. Leave the clearing")
    choice = input("Enter your choice: ")

    if choice == "1":
        print("The chest contains a magical amulet. You take it.")
        game_state.character.add_item("Magical Amulet")
        game_state.update_position("end")
    elif choice == "2":
        print("You rest and regain some health.")
        game_state.character.health = min(100, game_state.character.health + 20)
        game_state.update_position("clearing")
    elif choice == "3":
        print("You leave the clearing and continue your adventure.")
        game_state.update_position("end")
    else:
        print("Invalid choice, try again.")
        clearing_story(game_state)

story_paths["clearing"] = clearing_story

# Main game loop
def main():
    game_state = GameState()
    game_state.character = create_character()

    while True:
        display_status(game_state.character)
        story_function = story_paths.get(game_state.story_position)
        if story_function:
            story_function(game_state)
        else:
            print("The story ends here. Thank you for playing!")
            break

if __name__ == "__main__":
    main()
