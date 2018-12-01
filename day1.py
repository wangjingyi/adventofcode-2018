import itertools

def solution1():
    return sum(freq_changes())
    
def solution2():
    cur_freq = 0
    s = {cur_freq}
    source = itertools.cycle(freq_changes())
    for e in source:
        cur_freq += e
        if cur_freq in s:
            return cur_freq
        else:
            s.add(cur_freq)

    return None

def freq_changes():
    with open('input.txt') as f:
        return [int(line.strip()) for line in f]
        