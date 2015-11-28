import math
import sys

# Global variables


list_of_hostage = []
list_of_zombies = []

# Functions


def jump_closer_to_hostage():
        list_of_hostage.sort(key=lambda hostage: hostage.save_rank)
        debug("closest : " + str(list_of_hostage[0]))
        print(str(list_of_hostage[0].x) + " " + str(list_of_hostage[0].y))


def jump_closer_to_zombie():
        list_of_zombies.sort(key=lambda zombie: zombie.distance_from_james[1])
        debug("closest : " + str(list_of_zombies[0]))
        print(str(list_of_zombies[0].next_x) + " " + str(list_of_zombies[0].next_y))


def get_closest_zombie(hostage):
    closest_zombie = None
    distance = sys.maxsize
    for zombie in list_of_zombies:
        if zombie.distance_from_hostages[hostage.id][1] < distance:
            closest_zombie = zombie
            distance = zombie.distance_from_hostages[hostage.id][1]
    return closest_zombie


def number_zombies_around(is_current_distance, distance):
    no_zombies = 0
    for zombie in list_of_zombies:
        if is_current_distance:
            if zombie.distance_from_james[0] < distance:
                no_zombies += 1
        else:
            if zombie.distance_from_james[1] < distance:
                no_zombies += 1
    return no_zombies


def debug(string):
    print(string, file=sys.stderr)


def print_move(james_x, james_y):
    return debug(str(james_x) + " " + str(james_y))

# Classes


class Human(object):
    def __init__(self, humans_id, humans_x, humans_y):
        self.x = humans_x
        self.y = humans_y
        self.id = humans_id
        self.distance_from_james = -1
        self.distance_from_closest_zombie = -1
        self.save_rank = 16000

    def __str__(self):
        return "Human id: " + str(self.id) + ", (x,y) : " + str(self.x) + "," + str(self.y) + ", rank: " + str(self.save_rank)

    def calculate_move(self, nos_zombies, nos_hostages):
        nos_zmbs_arnd_james = number_zombies_around(False, 400)
        if nos_zmbs_arnd_james > (nos_zombies / 2):
            # print_move(self.x, self.y)
            print("I am waiting!!!")
        elif (nos_zombies / nos_hostages) >= 1:
            jump_closer_to_hostage()
        else:
            jump_closer_to_zombie()

    def calculate_distances(self, mr_james):
        distance_curr_from_james = math.hypot(mr_james.x - self.x, mr_james.y - self.y)
        self.distance_from_james = distance_curr_from_james
        debug("Hostage : " + str(self.id) + " distance to james: " + str(self.distance_from_james))

    def calculate_distance_frm_zombie(self, closest_zombie):
        distance_from_closest_zombie = math.hypot(closest_zombie.next_x - self.x, closest_zombie.next_y - self.y)
        self.distance_from_closest_zombie = distance_from_closest_zombie
        self.save_rank = self.save_rank - self.distance_from_closest_zombie + self.distance_from_james


class Zombie(object):
    def __init__(self, zombies_id, zombies_x, zombies_y, zombies_next_x, zombies_next_y):
        self.x = zombies_x
        self.y = zombies_y
        self.next_x = zombies_next_x
        self.next_y = zombies_next_y
        self.id = zombies_id
        self.distance_from_hostages = {}
        self.distance_from_james = (-1, -1)

    def __str__(self):
        return "Zombie: id-> " + str(self.id) + " , (x,y) : (" + str(self.x) + "," + str(self.y) + ") and next: (" + str(self.next_x) + "," + str(self.next_y) + ")"

    def calculate_distances(self, mr_james):
        self.distance_from_hostages = {}
        debug("Zombie: " + str(self.id))
        for hostage in list_of_hostage:
            distance_current = math.hypot(hostage.x - self.x, hostage.y - self.y)
            distance_next = math.hypot(hostage.x - self.next_x, hostage.y - self.next_y)
            debug("Hostage: " + str(hostage.id) + " distance_curr: " + str(distance_current) + ", distance_next: " + str(distance_next))
            self.distance_from_hostages[hostage.id] = (distance_current, distance_next)

        distance_curr_from_james = math.hypot(mr_james.x - self.x, mr_james.y - self.y)
        distance_next_from_james = math.hypot(mr_james.x - self.next_x, mr_james.y - self.next_y)
        self.distance_from_james = (distance_curr_from_james, distance_next_from_james)
        debug("distance to james: " + str(self.distance_from_james))
# Save humans, destroy zombies!

# game loop
while 1:

    list_of_hostage = []
    list_of_zombies = []

    x, y = [int(i) for i in input().split()]

    james_bond = Human("007", x, y)

    human_count = int(input())

    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
        list_of_hostage.append(Human(human_id, human_x, human_y))
        list_of_hostage[i].calculate_distances(james_bond)

    zombie_count = int(input())
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
        list_of_zombies.append(Zombie(zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext))
        list_of_zombies[i].calculate_distances(james_bond)

    for i in range(human_count):
        list_of_hostage[i].calculate_distance_frm_zombie(get_closest_zombie(list_of_hostage[i]))

    debug("My pos: x: " + str(x) + ", y: " + str(y) + ", human_count: " +  str(human_count) + ", zombies_count: " +  str(zombie_count))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Your destination coordinates
    james_bond.calculate_move(zombie_count, human_count)
