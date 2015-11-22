import random as rand
import sys

'''
Useful Function
'''

direction_list = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
direction_list_functions = ["move_north", "move_north_east", "move_east", "move_south_east",
                            "move_south", "move_south_west", "move_west", "move_north_west"]


def debug(string):
    print(string, file=sys.stderr)


def get_random_direction(skip):
    direction = ""

    while direction != skip:
        rand_index = rand.randint(0, 7)
        direction = direction_list[rand_index]
    return direction


def is_giant_around(giant_x, giant_y, thor_obj, min_distance=4):
    value_x = thor_obj.x - giant_x
    value_y = thor_obj.y - giant_y
    giant_direction = ""

    if value_x < 0:
        giant_direction = "S" + giant_direction
    else:
        giant_direction = "N" + giant_direction

    if value_y < 0:
        giant_direction = "E" + giant_direction
    else:
        giant_direction = "W" + giant_direction

    distance = max(abs(value_x), abs(value_y))
    return distance, distance < min_distance, giant_direction


def is_any_giant_around(the_thor, min_distance):
    for giant in giants_position:
        func_return_val = is_giant_around(giant[0], giant[1], the_thor, min_distance)
        if func_return_val[1]:
            return True
    return False

################################################################################


class Thor(object):
    def __init__(self, thor_x, thor_y):
        self.x = thor_x
        self.y = thor_y
        self.direction = "E"
        self.giants_around = []

    def __str__(self):
        return "Thor: [" + str(self.x) + "," + str(self.y) + "]"

    def min_distance_giant(self):
        min_distance = 40
        for giant_value in self.giants_around:
            if giant_value[0] < min_distance:
                min_distance = giant_value[0]
        return min_distance

    def move_north(self):
        if self.y > 0:
            self.y -= 1
            if is_any_giant_around(self, 2):
                self.y += 1
                return False
            else:
                print("N")
                return True
        return False

    def move_north_east(self):
        if self.y > 0 and self.x < (max_x - 1):
            self.x += 1
            self.y -= 1
            if is_any_giant_around(self, 2):
                self.x -= 1
                self.y += 1
                return False
            else:
                print("NE")
                return True
        return False

    def move_north_west(self):
        if self.y > 0 and self.x > 0:
            self.x -= 1
            self.y -= 1
            if is_any_giant_around(self, 2):
                self.x += 1
                self.y += 1
                return False
            else:
                print("NW")
                return True
        return False

    def move_east(self):
        if self.x < (max_x - 1):
            self.x += 1
            if is_any_giant_around(self, 2):
                self.x -= 1
                return False
            else:
                print("E")
                return True
        return False

    def move_west(self):
        if self.x > 0:
            self.x -= 1
            if is_any_giant_around(self, 2):
                self.x += 1
                return False
            else:
                print("W")
                return True
        return False

    def move_south_west(self):
        if self.y < (max_y - 1) and self.x > 0:
            self.x -= 1
            self.y += 1
            if is_any_giant_around(self, 2):
                self.x += 1
                self.y -= 1
                return False
            else:
                print("SW")
                return True
        return False

    def move_south_east(self):
        if self.y < (max_y - 1) and self.x < (max_x - 1):
            self.x += 1
            self.y += 1
            if is_any_giant_around(self, 2):
                self.x -= 1
                self.y -= 1
                return False
            else:
                print("SE")
                return True
        return False

    def move_south(self):
        if self.y < (max_y - 1):
            self.y += 1
            if is_any_giant_around(self, 2):
                self.y -= 1
                return False
            else:
                print("S")
                return True
        return False

    def move(self, main_number_giants_around):
        can_move = False
        tries = 0

        while not can_move and (tries < len(direction_list_functions)):
            can_move = getattr(self, direction_list_functions[tries])()
            debug("" + direction_list_functions[tries] + ": " + str(can_move))
            tries += 1
        if not can_move:
            debug("XXX Problem no more moves possible, is main_number_giants_around: " + str(main_number_giants_around))
            if main_number_giants_around == 0:
                print("WAIT")
            else:
                if self.min_distance_giant() < 2:
                    print("STRIKE")
                else:
                    print("WAIT")
###############################################################################


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

max_x = 40
max_y = 18

tx, ty = [int(i) for i in input().split()]

thor = Thor(tx, ty)

giants_position = []

debug("tx: " + str(tx) + ", ty: " + str(ty))

# game loop
while 1:
    number_giants_around = 0

    # h: the remaining number of hammer strikes.
    # n: the number of giants which are still present on the map.
    h, n = [int(i) for i in input().split()]
    debug("Number of hits remaining : " + str(h))
    debug("Number of giants around : " + str(n))
    debug("Giant's position: ")
    debug(str(thor))

    thor.giants_around = []

    for i in range(n):
        x, y = [int(j) for j in input().split()]
        debug("Giant(" + str(i) + ") : " + str(x) + ", " + str(y))
        return_val = is_giant_around(x, y, thor)
        debug("is_giant_around : " + str(return_val))

        if return_val[1]:
            number_giants_around += 1
            thor.giants_around.append(return_val)
            giants_position.append((x, y))

    debug("Number of giants around: " + str(number_giants_around))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # The movement or action to be carried out: WAIT STRIKE N NE E SE S SW W or N
    if n == 1 and number_giants_around == n:
        debug("coming here 1")
        print("STRIKE")
    else:
        if number_giants_around == n:
            debug("coming here 2")
            print("STRIKE")
        else:
            thor.move(number_giants_around)