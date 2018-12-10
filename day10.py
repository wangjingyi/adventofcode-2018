from dataclasses import dataclass
import re

@dataclass
class Point:
    position: (int, int)
    velocity: (int, int)     
        
    def next(self, i):
        x1, y1 = self.position
        vx, vy = self.velocity
        
        return x1 + vx * i, y1 + vy * i
    
    @staticmethod
    def distance(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)
    
def solution1():
    points = list(data())    
    i = evolve(points)
    pr_message([point.next(i) for point in points])
    
def solution2():
    points = list(data())
    return evolve(points)
    
def evolve(points):
    positions = [point.position for point in points]
    
    i = 1
    cur = Point.distance(*get_boundry(positions))
        
    while True:
        positions = [point.next(i) for point in points]
        pos1, pos2 = get_boundry(positions)
        nxt = Point.distance(pos1, pos2)
        if nxt < cur:
            i += 1
            cur = nxt
        else:
            break

    return i - 1

def get_boundry(positions):
    min_x, _ = min(positions, key = lambda p: p[0])
    max_x, _ = max(positions, key = lambda p: p[0])
    _, min_y = min(positions, key = lambda p: p[1])
    _, max_y = max(positions, key = lambda p: p[1])
    
    return (min_x, min_y), (max_x, max_y)

def pr_message(positions):
    (min_x, min_y), (max_x, max_y) = get_boundry(positions)
    pos = set(positions)
    
    for y in range(min_y, max_y + 1):
        s = []
        for x in range(min_x, max_x + 1):
            if (x, y) in pos:
                s.append('#')
            else:
                s.append('.')
        print(''.join(s))
        
def data():
    reg = re.compile(r'position=<([-\s]\d+),\s+([-\s]\d+)> velocity=<([-\s]\d+),\s+([-\s]\d+)>')
    with open('data/input_day10.txt') as f:
        for line in f:
            x, y, vx, vy = [int(g) for g in reg.match(line).groups()]
            yield Point((x, y), (vx, vy))
            