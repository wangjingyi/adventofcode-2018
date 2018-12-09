from dataclasses import dataclass, field

def solution1():
    return play(424 , 71482)

def solution2():
    return play(424, 71482 * 100)

@dataclass
class Node:
    value: int
    next: 'Node' = field(init=False, default=None)
    prev: 'Node' = field(init=False, default=None)
    
def play(num_of_player, last_point):
    players = [0] * num_of_player
    ring = DoubleList()
    
    for point in range(1, last_point + 1):
        idx = (point - 1) % num_of_player
        players[idx] += ring.next_put(point)
    
    return max(players)

# too much delete and insert, so double linked list should be a good way to go
class DoubleList:
    def __init__(self):
        self.root = Node(0)
        self.root.next = self.root
        self.root.prev = self.root
        
    def move(self, *, step=1, clockwise=True):    
        if clockwise:
            while step > 0:
                self.root = self.root.next
                step -= 1
        else:
            while step > 0:
                self.root = self.root.prev
                step -=1
        return self.root
    
    def add_node(self, value, back=True):
        node = Node(value)
        cur = self.root
        if back:
            node.prev = cur
            node.next = cur.next
            cur.next.prev = node
            cur.next = node
        else: 
            node.next = cur
            node.prev = cur.prev
            cur.prev.next = node
            cur.prev = node

        self.root = node
    
    def remove_node(self):
        deleted = self.root
        self.root = self.root.next
        deleted.prev.next = deleted.next
        deleted.next.prev = deleted.prev
        deleted.prev = None
        deleted.next = None
        return deleted
            
    def next_put(self, elem):
        score = 0
        if elem % 23 == 0:
            self.move(step=7, clockwise=False)
            deleted = self.remove_node()
            score += elem + deleted.value
        else:
            self.move()
            self.add_node(elem)
        
        return score       