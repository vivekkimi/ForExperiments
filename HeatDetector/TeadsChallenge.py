import sys
import math


def debug(data):
    print("Dbg: " + str(data), file=sys.stderr)
    
class Node(object):
    def __init__(self, value):
        self._link_nodes = []
        self._value = value
        self.level = 0
        
    def __eq__(self, other):
        return self._value == other
    
    def __contains__(self,value):
        return value == self._value

    def list_values(self):
        string =  "["
        for node in self._link_nodes:
            string += '(' + str(node._value) + ',' + str(node.level) + ')' + "," 
        return string + "]"

    def __str__(self):
        return "Node[ value: "+ str(self._value) + "," + "level: " + str(self.level) + "]"#+ " linkNodes: "+ self.list_values()+ " ]" 
    
    def __repr__(self):
        return str(self)
    
    def update_child_level(self):
        debug("Parent value: " + str(self._value))
        debug("Parent level: " + str(self.level))
        
        for node in self._link_nodes:
            node.level = self.level + 1
            node.update_child_level()

node_list = []  
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
max_level_reached = 0

n = int(input())  # the number of adjacency relations
for i in range(n):
    # xi: the ID of a person which is adjacent to yi
    # yi: the ID of a person which is adjacent to xi
    xi, yi = [int(j) for j in input().split()]
    
    n1 = xi
    n2 = yi
    
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
        node_2.level = node_1.level + 1
        
        node_2.update_child_level()
        
        if node_2.level > max_level_reached : 
            max_level_reached = node_2.level
        
        node_1._link_nodes.append(node_2)
        node_2._link_nodes.append(node_1)
        
    else:
        debug("One of the node is None!!!! Boom!!!!")
    
    max_length = -1
    max_node = None

debug("Node_list: " +  str(node_list))        

for node in node_list:
    if len(node._link_nodes) > max_length:
        max_length = len(node._link_nodes)
        max_node = node

jumps_needed = 0
if (max_level_reached - max_node.level) > max_node.level :
    jumps_needed = max_level_reached - max_node.level
else:
    jumps_needed = max_node.level
    
print(jumps_needed)        
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

# The minimal amount of steps required to completely propagate the advertisement
# print("1")
