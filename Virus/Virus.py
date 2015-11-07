import sys
import math


def error(data):
    print("Err: " + str(data), file=sys.stderr)
    
def debug(data):
    print("Dbg: " + str(data), file=sys.stderr)
    
class Node(object):
    def __init__(self, value):
        self._link_nodes = []
        self._value = value
        self._is_exit = False
        self._is_virus = False
        
    def __eq__(self, other):
        return self._value == other
    
    def __contains__(self,value):
        return value == self._value

    def list_values(self):
        string =  "["
        for node in self._link_nodes:
            string += str(node._value) + "," 
        return string + "]"

    def __str__(self):
        return "Node[ value: "+ str(self._value) + ", isExit: "+ str(self._is_exit) + ", isVirus: "+ str(self._is_virus) + " linkNodes: "+ self.list_values()+ " ]" 
    
    def __repr__(self):
        return str(self)

node_list = []    
exit_node_index = []
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
n, l, e = [int(i) for i in input().split()]

for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
    
    debug(str(n1)+"-->"+str(n2))
    
    node_1 = None
    node_2 = None
    
    if n1 not in node_list:
        node_1 = Node(n1)
        node_list.append(node_1)
    else:
        node_1 = node_list[node_list.index(n1)]
        
    if n2 not in node_list:
        node_2 = Node(n2)
        node_list.append(node_2)
    else:
        node_2 = node_list[node_list.index(n2)]
        
    if node_1 != None and node_2 != None:    
        node_1._link_nodes.append(node_2)
        node_2._link_nodes.append(node_1)
    else:
        error("One of the node is None!!!! Boom!!!!")
            
for i in range(e):
    ei = int(input())  # the index of a gateway node
    node_list[node_list.index(ei)]._is_exit = True
    exit_node_index.append(ei)

# debug(node_list)

prev_skynet_pos = None
# game loop
while 1:
    
    if prev_skynet_pos != None:
        node_list[node_list.index(prev_skynet_pos)]._is_virus = False
        
    si = int(input())  # The index of the node on which the Skynet agent is positioned this turn

    debug("Skynet: " + str(si))
    skynet_node = None
    skynet_node = node_list[node_list.index(si)]
    
    debug("exit nodes : " + str(exit_node_index))
#     debug("Skynet: " + str(si))
    debug("Skynet Node: " + str(skynet_node))
    
    skynet_node._is_virus = True
    
    severed_from = None
    severed_to = None
    
    for exit_index in exit_node_index:
        debug("checking for exit node: " + str(exit_index))
        if exit_index in skynet_node._link_nodes:
            severed_from = si
            severed_to = exit_index
            break
        else:
            exit_node = node_list[node_list.index(exit_index)]
            debug("exit_node : "+ str(exit_node))
            for link_node in exit_node._link_nodes:
                if si in link_node._link_nodes:
                    severed_from = link_node._value
                    severed_to = exit_index
        debug("End of loop: "+ str(severed_from) + "-->" + str(severed_to))
    prev_skynet_pos = si
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    debug("Severed: "+ str(severed_from)+" "+str(severed_to))
    print(str(severed_from)+" "+str(severed_to))
    # Example: 0 1 are the indices of the nodes you wish to sever the link between
#     print("0 1")
