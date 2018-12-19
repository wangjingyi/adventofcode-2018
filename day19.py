INPUT=r"""#ip 5
addi 5 16 5
seti 1 3 1
seti 1 1 2
mulr 1 2 4
eqrr 4 3 4
addr 4 5 5
addi 5 1 5
addr 1 0 0
addi 2 1 2
gtrr 2 3 4
addr 5 4 5
seti 2 4 5
addi 1 1 1
gtrr 1 3 4
addr 4 5 5
seti 1 5 5
mulr 5 5 5
addi 3 2 3
mulr 3 3 3
mulr 5 3 3
muli 3 11 3
addi 4 8 4
mulr 4 5 4
addi 4 13 4
addr 3 4 3
addr 5 0 5
seti 0 8 5
setr 5 3 4
mulr 4 5 4
addr 5 4 4
mulr 5 4 4
muli 4 14 4
mulr 4 5 4
addr 3 4 3
seti 0 8 0
seti 0 4 5"""

from dataclasses import dataclass, field
from typing import List, Dict, Callable, Tuple
import operator, re

@dataclass
class Device:
    registers: List[int] = field(init=False)
    commands: Dict[str, Callable[[int, int], int]] = field(init=False, repr=False)
    bound_reg: int = field(repr=False)
    program: List[Tuple[str, int, int, int]] = field(repr=False)
    
    def __init__(self, reg, program):
        self.bound_reg = reg
        self.program = program
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
        self.registers = [0, 0, 0, 0, 0, 0]
           
    @property
    def ip(self):
        return self.registers[self.bound_reg]
    
    def incr_ip(self):
        self.registers[self.bound_reg] += 1
        
    def run(self):
        while True:
            try:
                cmd, a, b, c = self.program[self.ip]
                print(f'ip#{self.ip}', cmd, a, b, c, f'{self.registers}')
            except IndexError:
                break
            self.execute(cmd, a, b, c)
            self.incr_ip()                     
         
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

def solution1():
    reg, program = data()
    d = Device(reg, program)
    d.run()
    return d.registers[0]

def solution2():
    r3 = 10551425
    return sum(i for i in range(1, r3 + 1) if r3 % i == 0)   
    
def data():
    lines = INPUT.splitlines()
    reg, *_ = re.match(r"#ip\s+(\d+)", lines[0]).groups()
    
    ret = []
    for line in lines[1:]:
        cmd, a, b, c = re.match(r"(\w+)\s+(\d+)\s+(\d+)\s+(\d+)", line).groups()
        ret.append((cmd, int(a), int(b), int(c)))
    return int(reg), ret
