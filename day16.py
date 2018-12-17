from dataclasses import dataclass, field
from typing import List, Dict, Callable
import operator, re

@dataclass
class Device:
    registers: List[int] = field(init=False)
    commands: Dict[str, Callable[[int, int], int]] = field(init=False, repr=False)
    
    def __init__(self):
        self.commands = {
            'addr': operator.add,
            'addi': operator.add,
            'mulr': operator.mul,
            'muli': operator.mul,
            'banr': operator.and_,
            'bani': operator.and_,
            'borr': operator.or_,
            'bori': operator.or_,
            'gtir': operator.gt,
            'gtri': operator.gt,
            'gtrr': operator.gt,
            'eqir': operator.eq,
            'eqri': operator.eq,
            'eqrr': operator.eq,
            'setr': None,
            'seti': None
        }
        self.registers = [0, 0, 0, 0]
        
    def reinit(self, registers):
        self.registers = registers
    
    def execute(self, cmd, a, b, c):
        if cmd in ('seti', 'setr'):
            self.registers[c] = self.registers[a] if cmd[-1] == 'r' else a
            return
        
        op = self.commands[cmd]
        if cmd[:-1] in ('add', 'mul', 'ban', 'bor'):
            other = self.registers[b] if cmd[-1] == 'r' else b
            self.registers[c] = op(self.registers[a], other)
        else:
            x = self.registers[a] if cmd[-2] == 'r' else a
            y = self.registers[b] if cmd[-1] == 'r' else b
            self.registers[c] = 1 if op(x, y) else 0
    
    def count(self, before, operands, after):
        cnt = 0
        op, a, b, c = operands
        s = set()
        for cmd in self.commands:
            self.reinit(before[:])
            self.execute(cmd, a, b, c)
            if self.registers == after:
                cnt += 1
                s.add(cmd)
        return cnt, (op, s)

def solution1():
    cnt = 0
    device = Device()
    for before, operands, after in data():
        howmany, _ = device.count(before, operands, after)
        if howmany >= 3:
            cnt += 1
    return cnt

def solution2():
    mapping = op()
    good = {k:v.pop() for k, v in mapping.items() if len(v) == 1 }
    candidates = {k: v for k, v in mapping.items() if len(v) > 1}
    while len(candidates) > 0:
        for v in good.values():
            for k, cv in candidates.items():
                if v in cv:
                    cv.remove(v)
        good.update({k: v.pop() for k, v in candidates.items() if len(v) == 1})
        candidates = {k: v for k, v in candidates.items() if len(v) > 1}

    device = Device()
    for cmd, *ops in data2():
        device.execute(good[cmd], *ops)
        
    return device.registers[0]

def op():
    device = Device()
    mapping = {}
    for before, operands, after in data():
        _, (op, s) = device.count(before, operands, after)
        if op in mapping:
            mapping[op] |= s
        else:
            mapping[op] = s
    return mapping

def data():
    lines = [r"Before:\s+\[(\d+, \d+, \d+, \d+)\]", r"(\d+\s\d+\s\d+\s\d+)", r"After:\s+\[(\d+, \d+, \d+, \d+)\]" ]
    reg = re.compile('\n'.join(lines), re.RegexFlag.MULTILINE)

    with open('data/input_day16_a.txt') as f:
        text = f.read()
    
    ret = []
    for match in reg.finditer(text):
        before, cmd, after = match.groups()
        before = [int(s) for s in before.split(', ')]
        cmd = tuple([int(s) for s in cmd.split(' ')])
        after = [int(s) for s in after.split(', ')]
        ret.append((before, cmd, after))
    
    return ret

def data2():
    ret = []
    with open('data/input_day16_b.txt') as f:
        for line in f:
            a, b, c, d = line.split(' ')
            ret.append((int(a), int(b), int(c), int(d)))
    return ret