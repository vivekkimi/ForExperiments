import sys
import math
from _ast import Str

def error(data):
    print("Err: " + str(data), file=sys.stderr)
    
def debug(data):
    print("Dbg: " + str(data), file=sys.stderr)
            
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in input().split()]
n = int(input())  # maximum number of turns before game over.
x0, y0 = [int(i) for i in input().split()]

debug("Matrix: " + str(w) + "x" + str(h))
debug("Max turns: " + str(n))
debug("current position: (" + str(x0) + "," + str(y0) + ")")

jump_x0 = 0 
jump_y0 = 0

jump_x1 = w-1
jump_y1 = h-1
# game loop
while 1:
    bomb_dir = input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
    
    debug("bomb_dir : " + bomb_dir)
    debug("Batman position : (" + str(x0) + "," + str(y0) + ")" )
    debug("x0,y0 : ("+ str(jump_x0) + "," + str(jump_y0) + ")")
    debug("x1,y1 : ("+ str(jump_x1) + "," + str(jump_y1) + ")")
    
    if bomb_dir == "U":
        jump_y1 = y0
        y0 -= round((y0 -jump_y0) / 2)
    
    if bomb_dir == "D":
        jump_y0 = y0
        y0 += int(math.ceil((jump_y1 - y0) / 2))
    
    if bomb_dir == "L":
        jump_x1 = x0
        x0 -= int(math.ceil((x0 -jump_x0) / 2))
    
    if bomb_dir == "R":
        jump_x0 = x0
        x0 += int(math.ceil((jump_x1 - x0) / 2))
    
    if bomb_dir == "UR":
        jump_y1 = y0
        y0 -= int(math.ceil((y0 -jump_y0) / 2))
        jump_x0 = x0
        x0 += int(math.ceil((jump_x1 - x0) / 2))
    
    if bomb_dir == "DR":
        jump_y0 = y0
        y0 += int(math.ceil((jump_y1 - y0) / 2))
        jump_x0 = x0
        x0 += int(math.ceil((jump_x1 - x0) / 2))
    
    if bomb_dir == "DL":
        jump_y0 = y0
        y0 += int(math.ceil((jump_y1 - y0) / 2))
        jump_x1 = x0
        x0 -= int(math.ceil((x0 -jump_x0) / 2))
    
    if bomb_dir == "UL":
        jump_x1 = x0
        x0 -= int(math.ceil((x0 -jump_x0) / 2))
        jump_y1 = y0
        y0 -= int(math.ceil((y0 -jump_y0) / 2))
        
    debug("Jumps: " + str(x0) + " " + str(y0))
    # the location of the next window Batman should jump to.
    print(str(x0) + " " + str(y0))
