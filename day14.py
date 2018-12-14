INPUT = 327901
def break_digits(num):
    q, r= divmod(num, 10)
    ret = [r]
    while q != 0:
        q, r = divmod(q, 10)
        ret.append(r)
    return list(reversed(ret))

def to_str(*digits):
    return ''.join([str(i) for i in digits])

def scores(a, b, stop=INPUT):
    idx_a = 0
    idx_b = 1
    ret = [a, b]
    
    while len(ret) < stop + 10:
        nsum = ret[idx_a] + ret[idx_b]
        digits = break_digits(nsum)
        ret.extend(digits)
        idx_a = (idx_a + ret[idx_a] + 1) % len(ret)
        idx_b = (idx_b + ret[idx_b] + 1) % len(ret)
    
    return ''.join([str(x) for x in ret[stop:stop+10]])

def search_score(a, b, needle=INPUT):
    idx_a, idx_b = 0, 1
    ret = [a, b]
    target = str(needle)
    holder = to_str(a, b)
    
    while not holder.startswith(target):
        nsum = ret[idx_a] + ret[idx_b]
        digits = break_digits(nsum)
        ret.extend(digits)
        idx_a = (idx_a + ret[idx_a] + 1) % len(ret)
        idx_b = (idx_b + ret[idx_b] + 1) % len(ret)
        
        s = to_str(*digits)
        ns = f'{holder}{s}'
        holder = ns if target.startswith(ns) else s
  
    return ''.join([str(x) for x in ret]).index(target)

def solution1():
    return scores(3, 7)

def solution2():
    return search_score(3, 7)