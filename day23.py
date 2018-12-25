from dataclasses import dataclass, field
from heapq import heappush, heappop
import operator, re
import networkx as nx

@dataclass(frozen=True)
class Nanobot:
    x: int 
    y: int
    z: int    
    radius: int = field(repr=False)
    
    @staticmethod
    def distance(p1, p2):
        return abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)
    
    def to_point(self, x, y, z):
        return abs(self.x - x) + abs(self.y - y) + abs(self.z - z)
    
    @staticmethod
    def touched(p1, p2):
        return Nanobot.distance(p1, p2) <= p1.radius + p2.radius
    
    def __iter__(self):
        for item in (self.x, self.y, self.z, self.radius):
            yield item
    
def data():
    reg = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>,\s+r=(\d+)')
    with open('data/input_day23.txt') as f:
        return [Nanobot(*tuple(map(int, reg.match(line.strip()).groups()))) for line in f]
    
def solution1():
    bots = data()
    max_bot = max(bots, key=operator.attrgetter('radius'))
    return sum(Nanobot.distance(max_bot, bot) <= max_bot.radius for bot in bots)
      
def solution2():
    graph = nx.Graph()
    bots = data()
    for bot1 in bots:
        for bot2 in bots:
            if Nanobot.touched(bot1, bot2):
                graph.add_edges_from([(bot1, bot2)]) # a list of tuple
    clique = max(list(nx.find_cliques(graph)), key=len)  # the most overlapped bots. bronker bosche algorithm
    return max([bot.to_point(0, 0, 0) - bot.radius for bot in clique])

# put the start and the end of a range into a queue sorted by the distance (distance, counter)
# the count variable will count the overlap region (if start a region, count will be incremented because of overlap. if end of a region
# the counter will be decremented because of a region is out of current counting)
# the start of maxcount will be shortest distance to the origin
    
# let's think of a belt shape (all across (0,0)) and count the most overlap belt shape.
# we can put 2 entries for each shape into a heap. (start_distance, +1) and (end_distance, -1)
# and then we just increment or decrement the counter.
# the smart solution is counting the overlap in 3 dimension.
def smartsolution():
    q = []
    for x, y, z, r in data():
        d = abs(x) + abs(y) + abs(z)
        heappush(q, (max(0, d - r), +1))  # +1 mark the start of the line segment
        heappush(q, (d + r, -1))  #-1 mark the end of the line segment
        
    count, maxcount, ret = 0, 0, 0
    while q:
        distance, marker = heappop(q)
        count += marker         #increase (marker=+1) if start the line segment, decrease(marker=-1) if the end of line segment
        if count > maxcount:    # better overlap
            ret = distance
            maxcount = count
    
    return ret