INPUT=r"""#ip 5
seti 123 0 1
bani 1 456 1
eqri 1 72 1
addr 1 5 5
seti 0 0 5
seti 0 0 1
bori 1 65536 2
seti 6663054 1 1
bani 2 255 4
addr 1 4 1
bani 1 16777215 1
muli 1 65899 1
bani 1 16777215 1
gtir 256 2 4
addr 4 5 5
addi 5 1 5
seti 27 6 5
seti 0 6 4
addi 4 1 3
muli 3 256 3
gtrr 3 2 3
addr 3 5 5
addi 5 1 5
seti 25 9 5
addi 4 1 4
seti 17 3 5
setr 4 4 2
seti 7 2 5
eqrr 1 0 4
addr 4 5 5
seti 5 8 5"""

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
        
    def run(self, which='part1'):
        seen = set()
        while True:
            try:
                cmd, a, b, c = self.program[self.ip]
                #print(f'ip#{self.ip}', cmd, a, b, c, f'{self.registers}')
            except IndexError:
                break
            if self.ip == 28:  #when ip == 28 and r1 == r0, it will get out of range
                if which == 'part1':
                    return self.registers[1]
                else:               
                    if self.registers[1] not in seen:
                        last_unqiue = self.registers[1]
                        seen.add(last_unqiue)
                    else:
                        return last_unqiue
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
    return d.run()

def solution2():
    reg, program = data()
    d = Device(reg, program)
    return d.run('part2')
    
def data():
    lines = INPUT.splitlines()
    reg, *_ = re.match(r"#ip\s+(\d+)", lines[0]).groups()
    
    ret = []
    for line in lines[1:]:
        cmd, a, b, c = re.match(r"(\w+)\s+(\d+)\s+(\d+)\s+(\d+)", line).groups()
        ret.append((cmd, int(a), int(b), int(c)))
    return int(reg), ret
