def solution():
    points = data()
    mapping = build_map(points)
    worker = list(mapping.values())
    
    for i, p1 in enumerate(points):
        for p2 in points[i+1:]:
            if distance(p1, p2) <= 3:
                union(mapping[p1], mapping[p2], worker)
                
    return count(worker)

def find(i, arr):
    updated = []
    while True:
        updated.append(i)
        if arr[i] == i:
            break
        i = arr[i]
    
    return i, updated

def union(i, j, arr):
    
    root_i, updated_i = find(i, arr)
    root_j, updated_j = find(j, arr)
    
    if root_i == root_j:
        return
    
    root = root_i if len(updated_i) > len(updated_j) else root_j
    
    for i in updated_i: #compression for group i
        arr[i] = root
    for j in updated_j: #compression for group j
        arr[j] = root
        
def count(arr):
    return sum(k == v for k, v in enumerate(arr)) # count roots
    
def distance(p1, p2):
    w1, x1, y1, z1 = p1
    w2, x2, y2, z2 = p2
    return abs(w1 - w2) + abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

def build_map(tuples):
    return {v:k for k, v in enumerate(tuples)}

def data():
    with open('data/input_day25.txt') as f:
        return [tuple(map(int, line.split(','))) for line in f]