import sys
import math
import numpy as np
from distutils.debug import DEBUG

#, X, @, $, S, E, N, W, B, I, T

dictionay = {"B" : 0, "S" : 1, "E" : 2, "N" : 3, "W" : 4, "I" : 5, "@" : 6, "$" : 7, "I" : 8, "T" : 9, "X" : 10, " " : 11, "#" : 12}

direction = ["S", "E", "N", "W"]

complete_moves_array = []

# need to save snapshots of the state and put it in the sets and then compare it whenever we make a move to ensure we do not come across same state configuration.
prev_move_states = set()

looping = False

class Robo(object):

    x = 0 
    y = 0
    max_len = 0
    max_col = 0
    
    def __init__(self, x, y, l, c):
        self.x = x
        self.y = y
        self._prev_move = None
        self._next_move = None
        self.is_inverted = False
        self.is_breaker_mode = False
        self.max_col = c
        self.max_len = l
    
    def get_snapshot(self):
        return (self.x, self.y, self.is_inverted, self.is_breaker_mode, self._prev_move, self._next_move)
        
    def __str__(self):
        return "Robot: _prev_move: " +  str(self._prev_move) + ", _next_move: " + str(self._prev_move) + ", is_breaker_mode: " + str(self.is_breaker_mode)

    def move_east(self):
        if self.y < (self.max_col - 1) :
#             if numpy_map[self.x][self.y + 1] == dictionay['$'] or numpy_map[self.x][self.y + 1] == dictionay['E'] or numpy_map[self.x][self.y + 1] == dictionay[' '] or numpy_map[self.x][self.y + 1] == dictionay['@']:
            if (self.is_breaker_mode or numpy_map[self.x][self.y + 1] != dictionay["X"]) and numpy_map[self.x][self.y + 1] != dictionay["#"]:
                self._prev_move = "E"
                
                self.y += 1
                
                if numpy_map[self.x][self.y] == dictionay["X"] and self.is_breaker_mode:
#                     debug("I have broken the wall, hence modify the value")
                    numpy_map[self.x][self.y] = dictionay[" "] 
                
                if getKeyByValue(numpy_map[self.x][self.y] , dictionay) in direction:
                    self._next_move = getKeyByValue(numpy_map[self.x][self.y] , dictionay)
                else:
                    self._next_move = 'E'
                
                if numpy_map[self.x][self.y] == dictionay['B']:
                    if not self.is_breaker_mode:
                        self.is_breaker_mode = True
                    else:
                        self.is_breaker_mode = False
                
                if numpy_map[self.x][self.y] == dictionay['I']:
                    if not self.is_inverted:
                        self.is_inverted = True
                    else:
                        self.is_inverted = False
                        
                if numpy_map[self.x][self.y] == dictionay['T']:
                    if self.x == first_transform_pos[0] and self.y == first_transform_pos[1]:
                        self.x = second_transform_pos[0]
                        self.y = second_transform_pos[1]
                    elif self.x == second_transform_pos[0] and self.y == second_transform_pos[1]:
                            self.x = first_transform_pos[0]
                            self.y = first_transform_pos[1]

#                 debug("EAST, " + str(self))
#                 print("EAST")
                complete_moves_array.append("EAST")
                return (True , None)
            
            debug("cannot move EAST, as it contains: " + str(getKeyByValue(numpy_map[self.x][self.y + 1], dictionay)))
            return (False , numpy_map[self.x][self.y + 1])
        
        return (False , None)
    
    def move_west(self):
        if self.y > 0 :
#             if numpy_map[self.x][self.y - 1] == dictionay['$'] or numpy_map[self.x][self.y - 1] == dictionay['W'] or numpy_map[self.x][self.y - 1] == dictionay[' ']:
            if (self.is_breaker_mode or numpy_map[self.x][self.y - 1] != dictionay['X']) and numpy_map[self.x][self.y - 1] != dictionay['#']:
                self._prev_move = "W"
                self.y -= 1
                
                if numpy_map[self.x][self.y] == dictionay["X"] and self.is_breaker_mode:
#                     debug("I have broken the wall, hence modify the value")
                    numpy_map[self.x][self.y] = dictionay[" "] 
                    
                if getKeyByValue(numpy_map[self.x][self.y] , dictionay) in direction:
                    self._next_move = getKeyByValue(numpy_map[self.x][self.y] , dictionay)
                else:
                    self._next_move = 'W'
                
                if numpy_map[self.x][self.y] == dictionay['B']:
                    if not self.is_breaker_mode:
                        self.is_breaker_mode = True
                    else:
                        self.is_breaker_mode = False

                if numpy_map[self.x][self.y] == dictionay['I']:
                    if not self.is_inverted:
                        self.is_inverted = True
                    else:
                        self.is_inverted = False
                        
                if numpy_map[self.x][self.y] == dictionay['T']:
                    debug("Transforming form : " + str(self.x) + "," + str(self.y))
                    if self.x == first_transform_pos[0] and self.y == first_transform_pos[1]:
                        
                        self.x = second_transform_pos[0]
                        self.y = second_transform_pos[1]
                    elif self.x == second_transform_pos[0] and self.y == second_transform_pos[1]:
                            self.x = first_transform_pos[0]
                            self.y = first_transform_pos[1]
                    debug("Transforming to : " + str(self.x) + "," + str(self.y))
                        
#                 debug("WEST, "+ str(self))
#                 print("WEST")
                complete_moves_array.append("WEST")
                return (True , None) 
            
            debug("cannot move WEST, as it contains: " + str(getKeyByValue(numpy_map[self.x][self.y - 1], dictionay)))
            return (False , numpy_map[self.x][self.y - 1])
        
        return (False , None)
    
    def move_south(self):
        if self.x < (self.max_len - 1) :
#             if numpy_map[self.x + 1][self.y] == dictionay['$'] or numpy_map[self.x + 1][self.y] == dictionay['S'] or numpy_map[self.x + 1][self.y] == dictionay[' ']:
            if (self.is_breaker_mode or numpy_map[self.x + 1][self.y] != dictionay['X']) and numpy_map[self.x + 1][self.y] != dictionay['#']:
                self._prev_move = "S"
                self.x += 1

                if numpy_map[self.x][self.y] == dictionay["X"] and self.is_breaker_mode:
#                     debug("I have broken the wall, hence modify the value")
                    numpy_map[self.x][self.y] = dictionay[" "] 
                
                if getKeyByValue(numpy_map[self.x][self.y] , dictionay) in direction:
                    self._next_move = getKeyByValue(numpy_map[self.x][self.y] , dictionay)
                else:
                    self._next_move = 'S'
                
                if numpy_map[self.x][self.y] == dictionay['B']:
                    if not self.is_breaker_mode:
                        self.is_breaker_mode = True
                    else:
                        self.is_breaker_mode = False
                        
                if numpy_map[self.x][self.y] == dictionay['I']:
                    if not self.is_inverted:
                        self.is_inverted = True
                    else:
                        self.is_inverted = False

                if numpy_map[self.x][self.y] == dictionay['T']:
                    if self.x == first_transform_pos[0] and self.y == first_transform_pos[1]:
                        self.x = second_transform_pos[0]
                        self.y = second_transform_pos[1]
                    elif self.x == second_transform_pos[0] and self.y == second_transform_pos[1]:
                            self.x = first_transform_pos[0]
                            self.y = first_transform_pos[1]
                        
#                 debug("SOUTH, "+ str(self))
#                 print("SOUTH")
                complete_moves_array.append("SOUTH")
                return (True , None) 
            
            debug("cannot move SOUTH, as it contains: " + str(getKeyByValue(numpy_map[self.x + 1][self.y], dictionay)))
            return (False , numpy_map[self.x + 1][self.y])
        
        return (False , None)
    
    def move_north(self):
        if self.x > 0 :
#             if numpy_map[self.x - 1][self.y] == dictionay['$'] or numpy_map[self.x - 1][self.y] == dictionay['N'] or numpy_map[self.x - 1][self.y] == dictionay[' ']:
            if (self.is_breaker_mode or numpy_map[self.x - 1][self.y] != dictionay['X']) and numpy_map[self.x - 1][self.y] != dictionay['#']:   
                self._prev_move = "N"
                self.x -= 1

                if numpy_map[self.x][self.y] == dictionay["X"] and self.is_breaker_mode:
                    debug("I have broken the wall, hence modify the value")
                    numpy_map[self.x][self.y] = dictionay[" "] 
                    
                if getKeyByValue(numpy_map[self.x][self.y] , dictionay) in direction:
                    self._next_move = getKeyByValue(numpy_map[self.x][self.y] , dictionay)
                else:
                    self._next_move = 'N'
            
                if numpy_map[self.x][self.y] == dictionay['B']:
                    if not self.is_breaker_mode:
                        self.is_breaker_mode = True
                    else:
                        self.is_breaker_mode = False
                        
                if numpy_map[self.x][self.y] == dictionay['I']:
                    if not self.is_inverted:
                        self.is_inverted = True
                    else:
                        self.is_inverted = False

                if numpy_map[self.x][self.y] == dictionay['T']:
                    if self.x == first_transform_pos[0] and self.y == first_transform_pos[1]:
                        self.x = second_transform_pos[0]
                        self.y = second_transform_pos[1]
                    elif self.x == second_transform_pos[0] and self.y == second_transform_pos[1]:
                            self.x = first_transform_pos[0]
                            self.y = first_transform_pos[1]
                        
#                 debug("NORTH, "+ str(self))
#                 print("NORTH")
                complete_moves_array.append("NORTH")
                return (True , None)
#             if numpy_map[self.x - 1][self.y] == dictionay['X'] or numpy_map[self.x - 1][self.y] == dictionay['#']:
#                 debug("cannot move NORTH, as it contains: " + str(getKeyByValue(numpy_map[self.x - 1][self.y], dictionay)))
#                 debug("Trying to move south")
#                 return try_ordered_direction('N') 
            return (False , numpy_map[self.x - 1][self.y])
        return (False , None)
    
def debug(data):
    print("Dbg: " + str(data), file=sys.stderr)

def getKeyByValue(value, dictionary):
    for a_key, a_value in dictionary.items():
        if a_value == value:
            return a_key

def try_ordered_direction(skip , is_reverse):
    
    is_move = (False ,  None)
    if not is_reverse:
        if skip != 'S':
            is_move = robot.move_south()
        if skip != 'E' and not is_move[0]:
            is_move = robot.move_east()
        if skip != 'N' and not is_move[0]:
            is_move = robot.move_north()
        if skip != 'W' and not is_move[0]:
            is_move = robot.move_west()
    else:
        if skip != 'W':
            is_move = robot.move_west()
        if skip != 'N' and not is_move[0]:
            is_move = robot.move_north()
        if skip != 'E' and not is_move[0]:
            is_move = robot.move_east()
        if skip != 'S' and not is_move[0]:
            is_move = robot.move_south()
    
    return is_move
   
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

l, c = [int(i) for i in input().split()]

numpy_map = np.zeros((l,c))

debug("Number of lines : "+ str(l) + " columns: "+str(c))
debug("-----------MAP----------")
for i in range(l):
    row = input()
    char_list = list(row)
    debug(str(row))
    for j in range(len(char_list)):
        numpy_map[i][j] = int(dictionay[char_list[j]])
debug("------------------------")

robo_pos = np.where(numpy_map == dictionay["@"])
robo_x = robo_pos[0][0]
robo_y = robo_pos[1][0]
debug("Position of Robo : "+ str(robo_x) + " and " + str(robo_y))

robot =  Robo(robo_x, robo_y, l, c)

transform_pos = np.where(numpy_map == dictionay["T"])
first_transform_pos = None
second_transform_pos = None
if len(transform_pos[0]) > 0:
    first_transform_pos = (transform_pos[0][0] , transform_pos[1][0])
    second_transform_pos = (transform_pos[0][1] , transform_pos[1][1])
    debug("Transformation position: first : " + str(first_transform_pos) + ", second: "+ str(second_transform_pos))

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
# debug("Map: "+ str(numpy_map))
# 
# debug(str(numpy_map[2][1]))
# debug(str(numpy_map[2][2]))
# debug(str(numpy_map[2][3]))
# not_moved_count = 0

loop_count = 0 
while True :
#     debug("robo position: "+ str(robot.x) + "," + str(robot.y))
#     debug("Numpy raw data at robo pos: "+ str(numpy_map[robot.x][robot.y]))
#     debug("data in numpy map for robo position: " + str(getKeyByValue(numpy_map[robot.x][robot.y], dictionay)))
    is_moved = (False ,  None)
    
    if numpy_map[robot.x][robot.y] == dictionay["$"]:
        is_moved = (False ,  None)
        debug("Reached the goal")
    else: 
        if (not is_moved[0] and robot._prev_move == None) or robot._next_move == "S":
            is_moved = robot.move_south()
        if robot._next_move == "E":
            is_moved = robot.move_east()
        if robot._next_move == "N":
            is_moved = robot.move_north()
        if robot._next_move == "W":
            is_moved = robot.move_west()
     
    if not is_moved[0]:
        if getKeyByValue(is_moved[1], dictionay) == '#' or (getKeyByValue(is_moved[1], dictionay) == 'X' and not robot.is_breaker_mode):
            debug("Its a block, go by priority")
            is_moved = try_ordered_direction(robot._prev_move , robot.is_inverted)

    if not is_moved[0]:
        break
    else:
        if robot.get_snapshot() not in prev_move_states:
            prev_move_states.add(robot.get_snapshot())
            loop_count = 0
            if(len(prev_move_states) > 30):
                prev_move_states = set()
        else:
            debug("Its looping : " + str(robot.get_snapshot()))
            debug("Move array : " + str(complete_moves_array))
            loop_count+=1
            if(loop_count > 4):
                looping = True
                break

if not looping:
    for direction in complete_moves_array:
        print(direction)
else:
        print("LOOP")
#         
#    
#     debug("is_moved: " + str(is_moved))
#     
#     if not is_moved : 
#         if not_moved_count < 3:
#             not_moved_count += 1
#         else:
#             break
#     else:
#         not_moved_count = 0