from operator import itemgetter

def compute(arr, start, end):
    acc = 0
    for i in range(start + 1, end):
        acc += arr[i]
    return min(arr[start], arr[end]) * (end - start - 1) - acc

def howmany(arr):
    index, value = max(list(enumerate(arr)), key=itemgetter(1))
    
    return left(arr[:index + 1]) + right(arr[index:])

def left(arr):
    acc = 0
    end = len(arr) - 1  
    while end != 0:
        index, value = max(list(enumerate(arr[:end])), key=itemgetter(1))
        acc += compute(arr, index, end)
        end = index

    return acc

def right(arr):
    acc = 0
    start = 0   
    while start != len(arr) - 1:
        index, value = max(list(enumerate(arr[start+1:], start=start+1)), key=itemgetter(1))
        acc += compute(arr, start, index)
        start = index
        
    return acc

assert compute([3, 0, 1, 3, 0, 5], 0, 2) == 1
assert compute([3, 0, 1, 3, 0, 5], 0, 3) == 5