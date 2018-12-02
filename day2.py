import collections

def solution1():
    twos, threes = 0, 0
    for id in data():
        s = set(collections.Counter(id).values())
        if 2 in s:
            twos += 1
        if 3 in s:
            threes += 1
    
    return twos * threes

def solution2():
    ids = data()
 
    for i, id1 in enumerate(ids):
        for id2 in ids[i + 1:]:
            flag, pos = one_difference(id1, id2)
            if flag:
                return id1[:pos] + id1[pos + 1:]
            
    return None
    

def one_difference(s1, s2):
    if len(s1) != len(s2):
        return False, None
    
    pos = None
    for i, pair in enumerate(zip(s1, s2)):
        fst, snd = pair
        if fst != snd and pos != None:
            return False, None
        elif fst != snd:
            pos = i
    else:
        return True, pos  # because must have one

            
        
def data():
    with open('input.txt') as f:
        return [line.strip() for line in f]