from dataclasses import dataclass, field
from collections import Counter

@dataclass(frozen=True)
class Point:
    y: int
    x: int
    max_x: int = field(default=50, init=False, repr=False)
    max_y: int = field(default=50, init=False, repr=False)
    
    def neigbors(self):
        return [Point(x = i, y = j) for j in (self.y - 1, self.y, self.y + 1)
                                    for i in (self.x - 1, self.x, self.x + 1) 
                                    if i in range(self.max_x) and j in range(self.max_y) and (self.x, self.y) != (i, j)]

def solution1():
    config = evolve(data(), times=10)
    return compute_area(config)

def solution2():
    config = data()
    frozen = frozenset(config.items())
    seen = {frozen: 0}
    found = False
    for i in range(1, 1000000000):
        config = evolve(config)
        frozen = frozenset(config.items())
        if frozen in seen:
            cycle = i - seen[frozen]
            found = True
        if found and 1000000000 % cycle == i % cycle:
            return compute_area(config)
        seen[frozen] = i
        
def compute_area(config):
    cnt = Counter()
    for v in config.values():
        if v == '#':
            cnt['#'] += 1
        elif v == '|':
            cnt['|'] += 1
    return cnt['#'] * cnt['|']
    
def step(point, current):
    count = Counter()
    for p in point.neigbors():
        count[current[p]] += 1
    typ = current[point]
    if typ == '.':
        return '|' if count['|'] >= 3 else typ
    elif typ == '|':
        return '#' if count['#'] >= 3 else typ
    else:
        return '#' if count['#'] >= 1 and count['|'] >= 1 else '.'
    
def evolve(config, times = 1):
    for i in range(times):
        nxt = {}
        for point in config.keys():
            nxt[point] = step(point, config)
        config = nxt
    
    return config

def data():
    with open('data/input_day18.txt') as f:
        return {Point(x=x, y=y) : ch for y, line in enumerate(f)
                                     for x, ch in enumerate(line.strip())}