from dataclasses import dataclass, field
from typing import List

@dataclass
class Node:
    childnum: int
    entrynum: int
    entries: List[int] = field(default_factory=list, init=False)
    children: List['Node'] = field(default_factory=list, init=False)

def solution1():
    root = get_root()
    return sum_node(root)
    
def sum_node(node):
    return sum(node.entries) + sum(sum_node(n) for n in node.children)
        
def solution2():
    root = get_root()
    return sum_node2(root)

def sum_node2(node):
    if len(node.children) == 0:
        return sum(node.entries)
    else:
        limit = len(node.children)
        return sum(sum_node2(node.children[idx - 1]) for idx in node.entries if idx <= limit)
    
def get_root():
    gen = data()
    root = next_node(gen)
    stack = [root]

    while len(stack) > 0:
        cur = stack.pop()
        if cur.childnum == 0:
            cur.entries = go_next(gen, step=cur.entrynum)
            if len(stack) > 0 :
                parent = stack.pop()
                parent.childnum -= 1
                parent.children.append(cur)
                stack.append(parent)
        else:
            stack.append(cur)
            stack.append(next_node(gen))
    return root
    
def next_node(g):
    return Node(*go_next(g))

def go_next(gen, step=2):
    next(gen)
    return gen.send(step)

def data():
    with open('data/input_day08.txt') as f:
        numbers = f.read().replace('\n', '').split(' ')
    
    start = 0
    while True:
        step = yield
        yield [int(e) for e in numbers[start:start + step]]
        start += step