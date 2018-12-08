import re
import collections

Rect = collections.namedtuple("Rect", "id x y w h")

def solution1():
    m = {}
    for rect in data():
        m = fill(rect, m)
    cnt = map(lambda s: s.count('x'), m.values())
    
    return sum(cnt)

def solution2():
    rects = data()
    for r1 in rects:
        for r2 in rects:
            if r1 is r2:
                continue
            if overlap(r1, r2):
                break
        else:
            return r1.id

    return None
    
def overlap(r1, r2):
    if r1.x > r2.x + r2.w - 1 or r2.x > r1.x + r1.w - 1:
        return False
    
    if r1.y > r2.y + r2.h - 1 or r2.y > r1.y + r1.h - 1:
        return False
    
    return True

def fill(rect, m):
    for row in range(rect.y, rect.y + rect.h):
        if row not in m:
            m[row] = f"{'.' * rect.x}{'o' * rect.w}"
        else:
            m[row] = update(rect, m[row])
    
    return m

def update(rect, row):
    length = rect.x + rect.w
    if len(row) < length:
        row += '.' * (length - len(row))
        
    ret = []
    for ch in row[rect.x:rect.x + rect.w]:
        if ch == '.':
            ret.append('o')
        else:
            ret.append('x')
        
            
    return row[:rect.x] + ''.join(ret) + row[rect.x + rect.w:]

def data():
    reg = re.compile(r"#(\d+)\s+@\s+(\d+),(\d+):\s+(\d+)x(\d+)")
    ret = []
    with open("data/input_day03.txt") as f:
        for line in f:
            tup = map(int, reg.match(line).groups())         
            ret.append(Rect(*tuple(tup)))
    return ret
