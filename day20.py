DIR = { 'N': (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0) }

def data():
    with open('data/input_day20.txt') as f:
        return f.read()
    
def solution1():
    s = data()
    rooms = explore(iter(s[1:]), (0, 0), {(0, 0): 0},0)
    return max(rooms.values())

def solution2():
    s = data()
    rooms = explore(iter(s[1:]), (0, 0), {(0, 0): 0}, 0)
    return sum(1 for v in rooms.values() if v >= 1000)

def explore(it, pos, rooms, distance):
    
    stack = []
    for ch in it:
        if ch == '$':
            return rooms
        elif ch in 'NWES':
            pos = (pos[0] + DIR[ch][0], pos[1] + DIR[ch][1])
            if pos in rooms:
                distance = rooms[pos]
            else:
                distance += 1
                rooms[pos] = distance
        elif ch == '(':
            stack.append((pos, distance))
        elif ch == '|':
            pos, distance = stack[-1]
        else:
            pos, distance = stack.pop()
        
     