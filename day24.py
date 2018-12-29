from dataclasses import dataclass, field
import re, operator, itertools

immune=r"""916 units each with 3041 hit points (weak to cold, fire) with an attack that does 29 fire damage at initiative 13
1959 units each with 7875 hit points (weak to cold; immune to slashing, bludgeoning) with an attack that does 38 radiation damage at initiative 20
8933 units each with 5687 hit points with an attack that does 6 slashing damage at initiative 15
938 units each with 8548 hit points with an attack that does 89 radiation damage at initiative 4
1945 units each with 3360 hit points (immune to cold; weak to radiation) with an attack that does 16 cold damage at initiative 1
2211 units each with 7794 hit points (weak to slashing) with an attack that does 30 fire damage at initiative 12
24 units each with 3693 hit points with an attack that does 1502 fire damage at initiative 5
2004 units each with 4141 hit points (immune to radiation) with an attack that does 18 slashing damage at initiative 19
3862 units each with 3735 hit points (immune to bludgeoning, fire) with an attack that does 9 fire damage at initiative 10
8831 units each with 3762 hit points (weak to radiation) with an attack that does 3 fire damage at initiative 7"""

infection=r"""578 units each with 55836 hit points with an attack that does 154 radiation damage at initiative 9
476 units each with 55907 hit points (weak to fire) with an attack that does 208 cold damage at initiative 18
496 units each with 33203 hit points (weak to fire, radiation; immune to cold, bludgeoning) with an attack that does 116 slashing damage at initiative 14
683 units each with 12889 hit points (weak to fire) with an attack that does 35 bludgeoning damage at initiative 11
1093 units each with 29789 hit points (immune to cold, fire) with an attack that does 51 radiation damage at initiative 17
2448 units each with 40566 hit points (immune to bludgeoning, fire; weak to cold) with an attack that does 25 slashing damage at initiative 16
1229 units each with 6831 hit points (weak to fire, cold; immune to slashing) with an attack that does 8 bludgeoning damage at initiative 8
3680 units each with 34240 hit points (immune to bludgeoning; weak to fire, cold) with an attack that does 17 radiation damage at initiative 3
4523 units each with 9788 hit points (immune to bludgeoning, fire, slashing) with an attack that does 3 bludgeoning damage at initiative 6
587 units each with 49714 hit points (weak to bludgeoning) with an attack that does 161 fire damage at initiative 2"""

@dataclass
class Group:
    side: int
    units: int
    hitpoints: int
    weak: [str]
    immune: [str]
    _damage: int
    damagetype: str
    initiative: int
    boost: int = field(init=None, default=0)
    attacker: 'Group' = field(init=None, default=None, repr=False)
    attackee: 'Group' = field(init=None, default=None, repr=False)
    
    @property
    def effective_power(self):
        return self.units * self.damage
    
    @property
    def damage(self):
        return self._damage + self.boost
    
    @property
    def target_order(self):
        return (-self.effective_power, -self.initiative)
    
    @property
    def attack_order(self):
        return -self.initiative
    
    @property
    def can_attack(self):
        return self.units > 0
    
    def chosen_order(self, damagetype):
        order = 1
        if damagetype in self.weak:
            order = 2
        elif damagetype in self.immune:
            order = 0
        return (-order, -self.effective_power, -self.initiative)
        
    def target(self, other):
        self.attackee = other
        other.attacker = self
        
    def attack(self, other):
        factor = 1
        if self.damagetype in other.weak:
            factor = 2
        elif self.damagetype in other.immune:
            factor = 0
        power = self.effective_power * factor
        
        killed_units = power // other.hitpoints
        if killed_units >= other.units:
            other.units = 0
            if other.attackee:
                other.attackee.attacker = None

        else:
            other.units -= killed_units
            
        self.attackee = None
        other.attacker = None
        
def target(arr):
    can_target = lambda g, o: g.damagetype not in o.immune
    good_ones = [g for g in arr if g.units > 0]
    for g in sorted(good_ones, key=operator.attrgetter('target_order')):
        opponents = sorted([o for o in good_ones if o.side != g.side and o.attacker is None and can_target(g, o)], key=operator.methodcaller('chosen_order', damagetype=g.damagetype))
        if opponents:
            g.target(opponents[0])
            
def attack(arr):
    good_ones = [g for g in arr if g.units > 0]
    for g in sorted(good_ones, key=operator.attrgetter('attack_order')):
        if g.attackee and g.can_attack:
            g.attack(g.attackee)
        
def solution1():
    _, units = once(parse_immune(), parse_infection())
    return units
    
def solution2():
    for boost in itertools.count():
        side, units = once(parse_immune(), parse_infection(), boost)
        if side == 0:
            return units

def once(immune, infection, boost=0):
    for g in immune:
        g.boost = boost
    arr = immune + infection
    
    old = (-1, -1)
    while True:
        target(arr)
        attack(arr)
        immune = sum([g.units for g in arr if g.side == 0])
        infection = sum([g.units for g in arr if g.side == 1])
        if infection == 0:
            return 0, immune
        elif old == (immune, infection):
            return 1, infection
        else:
            old = (immune, infection)
            
def parse_immune():
    return [parse(line.strip(), 0) for line in immune.splitlines()]

def parse_infection():
    return [parse(line.strip(), 1) for line in infection.splitlines()]
   
def parse(line, side):
    reg = re.compile(r'(\d+) units each with (\d+) hit points (\(.+\)\s+)?with an attack that does (\d+) (\w+) damage at initiative (\d+)')
    units, hits, paren, damage, damagetype, init = reg.match(line).groups()
    weak, im = [], []
    if paren:
        paren = paren.strip()[1:-1]
        if "weak" in paren and 'immune' in paren:
            arr = paren.split('; ')
            if 'weak' in arr[0]:
                weak = process(arr[0])
                im = process(arr[1])
            else:
                weak = process(arr[1])
                im = process(arr[0])
        elif "weak" in paren:
            weak = process(paren)
        else:
            im = process(paren)
        
    return Group(side=side, units=int(units), hitpoints=int(hits), weak=weak, immune=im, _damage=int(damage), damagetype=damagetype, initiative=int(init))

def process(sentence):
    reg = re.compile(r'(?:immune|weak) to (.+)$')  
    return reg.match(sentence).group(1).split(', ')