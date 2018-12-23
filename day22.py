from dataclasses import dataclass, field
from functools import lru_cache
from heapq import heappush, heappop

depth = 5355
target = (14, 796)

@dataclass(order=True)
class Point:
    f: int = field(init=False)
    x: int = field(compare=False)
    y: int = field(compare=False)
    tool : str = field(compare=False)
    g: int = field(init=False, compare=False, default=0)
    def cost(self, parent):
        if parent.tool == self.tool:
            return 1
        else:
            return 1 + 7
    
    def gscore(self, parent):
        "gscore = parent gscroe + real cost from parent to self"        
        return parent.g + self.cost(parent)
    
    def hscore(self): #admissible
        return abs(self.x - target[0]) + abs(self.y - target[1]) + (0 if self.tool == 'torch' else 7)
    
    def allowed(self, x, y):
        return self.tool in Point.tools((x,y))

    def neighbors(self):
        ps = []
        for x, y in [(self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y - 1), (self.x, self.y + 1)]:
            if x < 0 or y < 0 or not self.allowed(x, y):
                continue
            
            for tool in Point.tools((x, y)):
                ps.append(Point(x = x, y = y, tool = tool))
                
        for point in ps:
            point.g = point.gscore(self)
            point.f = point.g + point.hscore()
        
        return ps
    
    @property
    def key(self):
        return self.x, self.y, self.tool
    
    @staticmethod
    def tools(pos):
        t = region_type(pos)
        if t == 'rocky':
            return 'torch', 'gear'
        elif t == 'wet':
            return 'gear', 'neither'
        else:
            return 'torch', 'neither'
        
@lru_cache(maxsize=None)
def geo_index(pos):
    x, y = pos
    if pos in ((0, 0), target):
        return 0
    elif y == 0:
        return x * 16807
    elif x == 0:
        return y * 48271
    else:
        return eros_level((x - 1, y)) * eros_level((x, y - 1))

def eros_level(pos):
    return (geo_index(pos) + depth) % 20183

def region_type(pos):
    elevel = eros_level(pos) % 3
    if elevel == 0:
        return "rocky"
    elif elevel == 1:
        return "wet"
    else:
        return "narrow"

def risk_level(pos):
    typ = region_type(pos)
    if typ == 'rocky':
        return 0
    elif typ == 'wet':
        return 1
    else:
        return 2
    
def solution1():
    return sum(risk_level((x, y)) for x in range(0, target[0] + 1)
                                  for y in range(0, target[1] + 1))
    
def solution2():
    start = Point(0, 0, 'torch')
    start.f = start.hscore()
    
    queue = [start]    
    visited = set()
    
    while True:
        node = heappop(queue)
        if node.key == (*target, 'torch'):
            return node.f
        
        elif node.key in visited:
            continue
        
        visited.add(node.key)
        for p in node.neighbors():
            if p.key not in visited:
                heappush(queue, p)