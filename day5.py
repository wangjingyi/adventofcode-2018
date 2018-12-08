import string

def solution1():
    return react(data())

def solution2():
    s = data()
    return min(react(s, bad_unit=ch) for ch in string.ascii_lowercase)

def react(s, bad_unit = None):  
    if not s:
        return 0
    
    i = 0
    while bad_unit is not None and s[i].lower() == bad_unit:
        i += 1
        
    leftover = [s[i]]
    for ch in s[i + 1:]:
        if ch.lower() == bad_unit:
            continue
        
        if not leftover:
            leftover.append(ch)
        else:
            last = leftover.pop()
            if ch != last and ch.lower() == last.lower():
                continue
            else:
                leftover.extend((last, ch))
            
    return len(leftover)


def data():
    with open('data/input_day05.txt') as f:
        return f.read().replace('\n', '')
