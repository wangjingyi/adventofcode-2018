from collections import Counter, namedtuple, defaultdict
import re

Shift = namedtuple("Shift", 'minute cmd')

def solution1():
    amount, freq = arrange()
    id = max(amount, key=lambda k: sum(amount[k]))
    most_freq = freq[id].most_common(1)
    return int(id) * most_freq[0][0]

def solution2():
    amount, freq = arrange()
    freq = dict((k, v.most_common(1)[0]) for k, v in freq.items())   
    id = max(freq, key=lambda k: freq[k][1])
    return int(id) * freq[id][0]
        
def arrange():
    amount = defaultdict(list)
    freq = defaultdict(Counter)
    
    for shift in data():
        if shift.cmd.startswith("Guard"):
            id, *_ = re.findall(r"\d+", shift.cmd)
            current = amount[id]
        elif shift.cmd.startswith("falls"):
            start = int(shift.minute)
        else:
            end = int(shift.minute)
            current.append(end -start)
            s = freq[id]
            for minute in range(start, end):
                s[minute] += 1
    return amount, freq
    
def data():
    reg = re.compile("\[\d+-\d\d-\d\d\s+\d+:(\d+)\]\s(\w.+$)")
    with open('input.txt') as f:
        lines = [line for line in f]
        
    lines.sort()
    return [Shift(*reg.match(line).groups()) for line in lines]