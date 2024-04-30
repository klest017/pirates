import random
from game import config, event, location
from game import combat
from game.combat import Monster
from game.display import announce

class RockyIsland(location.Location):
    def __init__(self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Rocky Island"
        self.symbol = 'R'
        self.visitable = True
        self.starting_location = RockyShore(self)
        self.locations = {}
        self.locations["rockyShore"] = self.starting_location
        self.locations["rockyCave"] = RockyCave(self)
        # Add a new location for the puzzle
        self.locations["hiddenChamber"] = HiddenChamber(self)

    def enter(self, ship):
        print("You approach an island with rugged cliffs and crashing waves.")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class RockyShore(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "rockyShore"
        self.verbs['north'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 25
        self.events.append(RockfallEvent())

    def enter(self):
        description = "You land on the rocky shore of the island. Sharp rocks jut out of the water, and the sound of crashing waves fills the air."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            config.the_player.next_loc = self.main_location.locations["rockyCave"]
        elif verb == "east" or verb == "west":
            config.the_player.next_loc = self.main_location.locations["rockyShore"]

class RockyCave(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "rockyCave"
        self.verbs['exit'] = self
        self.event_chance = 100
        self.events.append(BearEvent())

    def enter(self):
        description = "You venture into a dark cave carved into the rocky cliffs. The air is cool and damp, and the sound of dripping water echoes off the walls."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "exit":
            config.the_player.next_loc = self.main_location.locations["rockyShore"]
            config.the_player.go = True

class RockfallEvent(event.Event):
    def __init__(self):
        self.name = "rockfall."

    def process(self, world):
        result = {}
        announce("A sudden rockfall blocks your path back to the ship!")
        config.the_player.next_loc = config.the_player.location
        config.the_player.go = False
        return result

class BearEvent(event.Event):
    def __init__(self):
        self.name = "bear encounter."

    def process(self, world):
        result = {}
        bear = Bear()
        announce("A ferocious bear emerges from the darkness and charges at you!")
        combat.Combat([bear]).combat()
        announce("The bear retreats back into the cave.")
        return result

class Bear(Monster):
    def __init__(self):
        attacks = {}
        attacks["claw"] = ["claws", random.randrange(40, 60), (10, 20)]
        super().__init__("Bear", random.randint(80, 120), attacks, 80 + random.randint(0, 20))

class HiddenChamber(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "hiddenChamber"
        self.verbs['inspect'] = self
        self.event_chance = 0  # No random events in the hidden chamber

    def enter(self):
        description = "You discover a hidden chamber deep within the cave, filled with ancient artifacts and mysterious symbols."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "inspect":
            # Display puzzle description and initiate puzzle-solving logic
            self.inspect_chamber()

    def inspect_chamber(self):
        puzzle_description = "You notice a series of symbols etched into the wall, hinting at a hidden mechanism."
        announce(puzzle_description)
        # Add logic here to handle the puzzle-solving process
        # For demonstration purposes, let's assume the player interacts with the symbols correctly
        self.solve_puzzle()

    def solve_puzzle(self):
        success_message = "You successfully decipher the symbols and unlock the hidden mechanism."
        announce(success_message)
        # Add logic here to progress the game or grant rewards upon solving the puzzle

# Create an instance of the RockyIsland to initiate the game
rocky_island = RockyIsland(0, 0, 0)
