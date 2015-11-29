import math
import sys

# Global variables

to_be_saved_human = None
list_of_hostage = []
list_of_zombies = []

# Functions


def jump_closer_to_hostage(james):
        list_of_hostage.sort(key=lambda hostage: hostage.new_rank_v2)
        debug("closest : " + str(list_of_hostage[0]))
        debug("James: " + str(james))
        debug("to be saved human: " + str(to_be_saved_human))
        # print(str(list_of_hostage[0].x) + " " + str(list_of_hostage[0].y))
        if len(list_of_hostage) > 1 and to_be_saved_human and to_be_saved_human.id == list_of_hostage[0].id and james.x == list_of_hostage[0].x and james.y == list_of_hostage[0].y:
            debug("Already SAVED!!! Mr. " + str(list_of_hostage[0].id))
            return list_of_hostage[1]
        return list_of_hostage[0]


def jump_closer_to_zombie():
        list_of_zombies.sort(key=lambda zombie: zombie.distance_from_james[1])
        # debug("closest : " + str(list_of_zombies[0]))
        # print(str(list_of_zombies[0].next_x) + " " + str(list_of_zombies[0].next_y))
        return list_of_zombies[0]


def get_closest_zombie(hostage):
    closest_zombie = None
    distance = sys.maxsize
    for zombie in list_of_zombies:
        if zombie.distance_from_hostages[hostage.id][1] < distance:
            closest_zombie = zombie
            distance = zombie.distance_from_hostages[hostage.id][1]
    return closest_zombie


def number_zombies_around(frm_human, is_current_distance, distance):
    no_zombies = 0
    for zombie in list_of_zombies:
        if is_current_distance:
            if frm_human.is_james:
                compare_distance = zombie.distance_from_james[0]
            else:
                compare_distance = zombie.distance_from_hostages[frm_human.id][0]
        else:
            if frm_human.is_james:
                compare_distance = zombie.distance_from_james[1]
            else:
                compare_distance = zombie.distance_from_hostages[frm_human.id][1]

        if compare_distance < distance:
            no_zombies += 1

    return no_zombies


def debug(string):
    print(string, file=sys.stderr)
    # return 0

def print_move(james_x, james_y):
    return print(str(james_x) + " " + str(james_y))

# Classes


class Human(object):
    def __init__(self, humans_id, humans_x, humans_y):
        self.x = humans_x
        self.y = humans_y
        self.id = humans_id
        self.distance_from_james = -1
        self.distance_from_closest_zombie = -1
        self.save_rank = 16000
        # self.to_be_saved_human = None
        self.new_rank = 16000
        self.new_rank_v2 = 16000
        self.is_james = False

    def __str__(self):
        return_str = "Human id: " + str(self.id) + ", (x,y) : " + str(self.x) + "," + str(self.y) + ", rank: " + str(self.new_rank)
        # if self.to_be_saved_human:
        #     return_str + ", to be saved: " + str(self.to_be_saved_human.id)
        return return_str

    def calculate_move(self, nos_zombies, nos_hostages):
        nos_zmbs_arnd_james = number_zombies_around(self, False, 2000)
        debug("nos_zmbs_arnd_james : " + str(nos_zmbs_arnd_james))
        # to_be_saved_human = None
        if nos_zmbs_arnd_james > (nos_zombies / 2):
            print_move(self.x, self.y)
            # print("I am waiting!!!")
        elif nos_zombies > 1 and  (nos_zombies / nos_hostages) >= 1:
            to_be_saved_human = jump_closer_to_hostage(self)
            print_move(to_be_saved_human.x, to_be_saved_human.y)
        else:
            zombie = jump_closer_to_zombie()
            print_move(zombie.x, zombie.y)
        return to_be_saved_human

    def calculate_distances(self, mr_james):
        distance_curr_from_james = math.hypot(mr_james.x - self.x, mr_james.y - self.y)
        self.distance_from_james = distance_curr_from_james
        # debug("Hostage : " + str(self.id) + " distance to james: " + str(self.distance_from_james))

    def calculate_rank(self, closest_zombie):
        distance_from_closest_zombie = math.hypot(closest_zombie.next_x - self.x, closest_zombie.next_y - self.y)
        self.distance_from_closest_zombie = distance_from_closest_zombie
        self.save_rank = self.save_rank - self.distance_from_closest_zombie + self.distance_from_james

        number_of_steps_required_by_zombie = distance_from_closest_zombie/400
        number_of_steps_required_by_james = self.distance_from_james / 1000

        debug("-------------------------------------")
        debug(str(self))
        debug(str(closest_zombie))
        debug("self.save_rank : " + str(self.save_rank))
        debug("distance_from_closest_zombie : " + str(distance_from_closest_zombie))
        debug("distance_from_james : " + str(self.distance_from_james))
        debug("number_of_steps_required_by_zombie : " + str(number_of_steps_required_by_zombie))
        debug("number_of_steps_required_by_james: " + str(number_of_steps_required_by_james))

        if number_of_steps_required_by_james < number_of_steps_required_by_zombie:
            self.new_rank *= (number_of_steps_required_by_james / number_of_steps_required_by_zombie)
        else:
            self.new_rank = self.save_rank * self.save_rank

        debug("self.new_rank : " + str(self.new_rank))

        number_of_zombies_around_me = number_zombies_around(self, False, 2000)
        self.new_rank_v2 = self.new_rank - (number_of_zombies_around_me * 1000)
        debug("number_of_zombies_around " + str(self.id) + " : " + str(number_of_zombies_around_me) + ", rank: " + str(self.new_rank_v2))
        debug("************************************************")

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
        # debug("Zombie: " + str(self.id))
        for hostage in list_of_hostage:
            distance_current = math.hypot(hostage.x - self.x, hostage.y - self.y)
            distance_next = math.hypot(hostage.x - self.next_x, hostage.y - self.next_y)
            # debug("Hostage: " + str(hostage.id) + " distance_curr: " + str(distance_current) + ", distance_next: " + str(distance_next))
            self.distance_from_hostages[hostage.id] = (distance_current, distance_next)

        distance_curr_from_james = math.hypot(mr_james.x - self.x, mr_james.y - self.y)
        distance_next_from_james = math.hypot(mr_james.x - self.next_x, mr_james.y - self.next_y)
        self.distance_from_james = (distance_curr_from_james, distance_next_from_james)
        # debug("distance to james: " + str(self.distance_from_james))
# Save humans, destroy zombies!

# game loop
while 1:

    list_of_hostage = []
    list_of_zombies = []

    x, y = [int(i) for i in input().split()]

    james_bond = Human("007", x, y)
    james_bond.is_james = True

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
        list_of_hostage[i].calculate_rank(get_closest_zombie(list_of_hostage[i]))

    debug("My pos: x: " + str(x) + ", y: " + str(y) + ", human_count: " + str(human_count) + ", zombies_count: " + str(zombie_count))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Your destination coordinates
    to_be_saved_human = james_bond.calculate_move(zombie_count, human_count)
