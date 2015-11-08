import heapq
import sys

import numpy as np

#--------------START GLOBAL VARS------------------
dictionary = {"#": 7, "?": 3, "C": 9, "T": 1, ".": 0}
direction = ["RIGHT", "UP", "LEFT", "DOWN"]


#--------------END GLOBAL VARIABLES----------------

''' A* Algorithm '''


class Cell(object):
    def __init__(self, x, y, reachable):
        """
        Initialize new cell
        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        if self.f < other.f:
            return -1
        elif self.f > other.f:
            return 1
        return 0

    def __str__(self):
        return "Cell(" + str(self.x)+ "," + str(self.y) + "): reachable: " + str(self.reachable)


class AStar(object):
    def __init__(self, max_row, max_col):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = max_row
        self.grid_width = max_col

    def init_grid(self, start_row, start_col, end_row, end_col):
        # debug("init_grid: " + str(locals()))
        for x in range(self.grid_height):
            for y in range(self.grid_width):
                if numpy_map[x][y] == dictionary['#']:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(start_row, start_col)
        debug("Start cell: " + str(self.start))
        self.end = self.get_cell(end_row, end_col)
        debug("End cell: " + str(self.end))

    def get_heuristic(self, cell):
        """
        Compute the heuristic value H for a cell: distance between
        this cell and the ending cell multiply by 10.
        @param cell
        @returns heuristic value H
        """
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        """
        Returns a cell from the cells list
        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x * self.grid_width + y]

    def get_adjacent_cells(self, cell):
        """
        Returns adjacent cells to a cell. Clockwise starting
        from the one on the right.
        @param cell get adjacent cells for this cell
        @returns adjacent cells list
        """
        cells = []
        if cell.x < self.grid_height-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_width-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def display_path(self):
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            debug('path: cell: %d,%d' % (cell.x, cell.y))

    def update_cell(self, adj, cell):
        """
        Update adjacent cell
        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            debug("Cell: " + str(cell) + " and " + str(cell is self.end))
            # if ending cell, display found path
            if cell is self.end:
                self.display_path()
                break
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))

''' Custom functions'''


def debug(string):
    print(string, file=sys.stderr)


def find_control_room():
    return np.where(numpy_map == dictionary["C"])

''' Class definitions '''


class Robo(object):
    init_x = 0
    init_y = 0
    x = 0
    y = 0
    max_row = 0
    max_col = 0
    prev_move = -1
    next_move = -1
    control_room_x = -1
    control_room_y = -1

    def __init__(self, init_x, init_y, max_row, max_col):
        self.init_x = self.x = init_x
        self.init_y = self.y = init_y
        self.max_col = max_col
        self.max_row = max_row

    def __str__(self):
        if not self.prev_move < 0:
            return "direction: " + direction[self.prev_move]
        return "Not initialized"

    def get_next_direction(self):
        self.next_move = (self.prev_move + 1) % 4
        return self.next_move

    def right(self):
        is_moved = False
        if self.y < (self.max_col - 1):
            if numpy_map[self.x][self.y + 1] == dictionary['#']:
                is_moved = False
            else:
                self.y += 1
                is_moved = True
        return is_moved

    def left(self):
        is_moved = False
        if self.y > 0:
            if numpy_map[self.x][self.y - 1] == dictionary['#']:
                is_moved = False
            else:
                self.y -= 1
                is_moved = True
        return is_moved

    def up(self):
        is_moved = False
        if self.x > 0:
            if numpy_map[self.x - 1][self.y] == dictionary['#']:
                is_moved = False
            else:
                self.x -= 1
                is_moved = True
        return is_moved

    def down(self):
        is_moved = False
        if self.x < (self.max_row - 1):
            if numpy_map[self.x + 1][self.y] == dictionary['#']:
                is_moved = False
            else:
                self.x += 1
                is_moved = True
        return is_moved

    def move(self):
        debug("robo: x and y : " + str(self.x) + " and " +  str(self.y))
        predicted_move = self.prev_move
        if predicted_move < 0:
            predicted_move = self.get_next_direction()

        control_room_coordinates = find_control_room()

        if len(control_room_coordinates[0]) > 0 and len(control_room_coordinates[1]) > 0:
            debug("Found Control Room: " + str(control_room_coordinates))
            self.control_room_x = control_room_coordinates[0][0]
            self.control_room_y = control_room_coordinates[1][0]
            debug("Call A* algorithm to find the route")
            astar = AStar(self.max_row, self.max_col)
            astar.init_grid(self.x, self.y, self.control_room_x, self.control_room_y)
            astar.process()

        else:
            is_moved = getattr(self, direction[predicted_move].lower())()
            if not is_moved:
                count = 0

                while not is_moved and count < 4:
                    predicted_move = self.get_next_direction()
                    is_moved = getattr(self, direction[predicted_move].lower())()
                    count += 1

            if not is_moved:
                debug("XXXX---> ERROR No Moves possible")

        debug("Direction Moved: " + direction[predicted_move])
        print(direction[predicted_move])

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# r: number of rows.
# c: number of columns.
# a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
r, c, a = [int(i) for i in input().split()]
numpy_map = np.zeros((r, c))
robo = Robo(-1, -1, r, c)

# game loop
while 1:
    # kr: row where Kirk is located.
    # kc: column where Kirk is located.
    kr, kc = [int(i) for i in input().split()]
    for i in range(r):
        row = input()  # C of the characters in '#.TC?' (i.e. one line of the ASCII maze).
        char_list = list(row)
        debug(str(row))
        for j in range(len(char_list)):
            numpy_map[i][j] = int(dictionary[char_list[j]])

    if robo.x < 0 and robo.y < 0:
        robo_pos = np.where(numpy_map == dictionary["T"])
        robo.x = robo_pos[0][0]
        robo.y = robo_pos[1][0]
    debug("Robots initial position, X: " + str(robo.x) + ", Y: " + str(robo.y))

    robo.move()

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Kirk's next move (UP DOWN LEFT or RIGHT).
    #print("RIGHT")
