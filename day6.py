import re
from collections import defaultdict, Counter

def solution1():
    d = data()
    left_top, right_bottom = get_corners(d)
    h = defaultdict(set)
    for point in d:
        for x in range(left_top[0], right_bottom[0] + 1):
            for y in range(left_top[1], right_bottom[1] + 1):
                fill((x, y), point, h)
          
    boundry = boundry_point(h, left_top, right_bottom)
    count = Counter()
    for v in h.values():
        if len(v) != 1:
            continue
        else:
            point = v.pop()
            if point not in boundry:
                count[point] += 1
    return count.most_common(1)

DISTANCE = 10000
def solution2():
    points = data()
    left_top, right_bottom = get_corners(points)

    x1, y1 = left_top
    x2, y2 = right_bottom
    
    ret = 0
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if close_enough((x, y), points, DISTANCE):
                ret += 1
                
    previous = ret  
    while True:
        for x in (x1 - 1, x2 + 1):
            for y in range(y1 - 1, y2 + 1 + 1):
                if close_enough((x, y), points, DISTANCE):
                    ret += 1
                    
        for y in (y1 - 1, y2 + 1):
            for x in range(x1, x2 + 1):
                if close_enough((x, y), points, DISTANCE):
                    ret += 1
                    
        if previous == ret:
            break   
        else:
            x1 -= 1
            x2 += 1
            y1 -= 1
            y2 += 1
            previous = ret
        
    return ret

def close_enough(point, all_points, distance):
    return sum(between(p, point) for p in all_points) < distance
    
def boundry_point(h, left_top, right_bottom):
    x1, y1 = left_top
    x2, y2 = right_bottom
    
    ret = set()
    for s in h.values():
        if len(s) == 1:
            e = next(iter(s))
            if e[0] in (x1, x2) or e[1] in (y1, y2):
                ret.add(e)
    return ret
    
    
def fill(location, point, h):

    s = h[location]
    if len(s) == 0:
        s.add(point)
    else:
        p2 = s.pop()
        if between(location, p2) < between(location, point):
            s.add(p2)
        elif between(location, p2) == between(location, point):
            s.update((point, p2))
        else:
            s.clear()
            s.add(point)

    return h
        
def get_corners(points):
    x, y = points[0]
    x1, y1, x2, y2 = x, y, x, y
    
    for x, y in points[1:]:
        if x < x1:
            x1 = x
        elif x > x2:
            x2 = x
            
        if y < y1:
            y1 = y
        elif y > y2:
            y2 = y
    
    return (x1, y1), (x2, y2)
        
        
def between(t1, t2):
    return abs(t2[1] - t1[1]) + abs(t2[0] - t1[0])

def data():
    r = re.compile(r'(\d+),\s+(\d+)')
    with open('data/input_day06.txt') as f:
        return [tuple(map(int, r.match(line).groups())) for line in f]
