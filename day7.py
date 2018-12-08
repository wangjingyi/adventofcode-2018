from collections import defaultdict 
import heapq, re

def solution1():
    queue, parent, children = build_queue()
    
    ret = []
    while queue:
       cur = heapq.heappop(queue)
       ret.append(cur)
       process_queue(queue, cur, parent, children)
       
    return "".join(ret)

NUM = 5
def solution2():
    queue, parent, children = build_queue()
    worker = [(0, None)] * NUM
    clock = 0
    
    while queue or worker.count((0, None)) != NUM:
        assign_work(worker, queue)
        t = process_work(worker, queue, parent, children)
        clock += t
        
    return clock

def assign_work(worker, queue):
    while worker.count((0, None)) != 0 and len(queue) != 0:
        cur = heapq.heappop(queue)
          
        for idx, (t, _) in enumerate(worker):
            if t == 0:
                worker[idx] = time(cur), cur
                break
                

                
def process_work(worker, queue, parent, children):
    if all([t == 0 for t, _ in worker]):
        return 0
    
    t, cur = min([(t, e) for t, e in worker if t > 0])
    for i, (time, elem) in enumerate(worker):
        if time == 0:
            continue
        worker[i] = time - t, None if time - t == 0 else elem
    
    process_queue(queue, cur, parent, children)  
    return t
    
def build_queue():
    dat = data()
    parent = defaultdict(set)
    children = defaultdict(set)
    for p, c in dat:
        children[p].update(c)
        parent[c].update(p)
    
    queue = list(set(children.keys()) - set(parent.keys()))
    heapq.heapify(queue)
    return queue, parent, children

def process_queue(queue, cur, parent, children):
    for child in children[cur]:
      parent[child].remove(cur)
      if not parent[child]:
        del parent[child]
        heapq.heappush(queue, child)     
        
def time(ch):
    return ord(ch) - ord('A') + 61
   
    
def data():
    reg = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin[.]')
    with open('input.txt') as f:
        return [reg.match(line.strip()).groups() for line in f]