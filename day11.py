import functools
from collections import defaultdict

SN = 7672

@functools.lru_cache(maxsize=None)
def fuel_power(x, y, sn):
    rack_id = x + 10
    start = rack_id * y
    tmp = (start + sn) * rack_id
    return (tmp // 100 ) % 10 - 5 
    
def grid_power1(x, y, sn=SN):
    if x + 3 > 301 or y + 3 > 301:
        return 0
    
    return sum(fuel_power(i, j, sn) for i in (x, x + 1, x + 2) for j in (y, y + 1, y + 2))

def solution1():
    return max((grid_power1(x, y), x, y) for x in range(1, 301 - 3) for y in range(1, 301 - 3))

def solution2():
    return grid_power()

#summed-area table
#all the area from the current point always to the left-top (0, 0)
def grid_power(sn=SN):
    m = defaultdict(int)
    
    # m contains area from (0, 0) to current point (x, y)
    # any boundry area like x = 0 or y = 0 will be 0 
    for x in range(2, 301 + 1):
        for y in range(2, 301 + 1):
            m[(x, y)] = m[(x - 1, y)] + m[(x, y - 1)] - m[(x - 1, y - 1)] + fuel_power(x - 1, y - 1, sn=sn)
            
    
    # now compute the square area based on the right-bottom coordinate
    # for any given size, (x, y) (the right-bottom coordinate) will start
    # at (size, size). for each given right_bottom point (x, y), the area with
    # size area(x, y) = area(x, y - s) + area(x - s, y) - area(x - s, y -s) + area(x - s, y - s)
    area = lambda x, y, s : m[(x, y)] - m[(x -s, y)] - m[x, (y - s)] + m[(x - s, y - s)]
    _, (x, y, size) = max((area(x, y, size), (x, y, size)) for size in range(1, 301) 
                                                 for x in range(size, 301 + 1) 
                                                 for y in range(size, 301 + 1))
    
    return (x - size), (y - size), size
    
#another way, all the area from current point to the bottom-right (301, 301)
def grid_power2(sn=SN):
    m = defaultdict(int)
    
    #compute area from current point (x, y) to the bottom-right point (301, 301) 
    for x in range(300, 0, -1):
        for y in range(300, 0, -1):
            m[(x, y)] = m[(x + 1, y)] + m[(x, y + 1)] - m[(x + 1, y + 1)] + fuel_power(x, y, sn)
           
    area = lambda x, y, s: m[(x, y)] - m[(x + s, y)] - m[(x, y + s)] + m[(x + s, y + s)]
    _, (x, y, size) =  max((area(x, y, size), (x, y, size)) for size in range(1, 301)
                                                            for x in range(1, 301)
                                                            for y in range(1, 301))
    return x, y, size