from dataclasses import dataclass, field
from collections import Counter

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)
ALL = [UP, RIGHT, DOWN, LEFT]
    
@dataclass
class Car:
    direction: 'Point'
    location: 'Point'
    switch: int = field(init=False, default=0, compare=False)
    iscollided: bool = field(init=False, default=False, compare=False)

    
    def to_left(self):
        left_idx = ALL.index(self.direction) - 1
        self.direction = ALL[left_idx]
    
    def to_right(self):
        right_idx = (ALL.index(self.direction) + 1) % len(ALL)
        self.direction = ALL[right_idx]
    
    def to_straight(self):
        self.location += self.direction
        
    def go_next(self, commands):
        if self.iscollided:
            return 
        
        self.to_straight()
            
        command = commands[self.location]

        if command == '/':
            if self.direction in (LEFT, RIGHT):
               self.to_left()
            else:
                self.to_right()
        elif command == '\\':
            if self.direction in (LEFT, RIGHT):
                self.to_right()
            else:
                self.to_left()
        elif command == '+':
            if self.switch == 0:
                self.to_left()
            elif self.switch == 2:
                self.to_right()
            self.switch = (self.switch + 1) % 3
            
def solution1():
    cars, commands = data()  
    collided, point = collide(cars)
    
    while not collided:
        cars = sorted(cars, key = lambda c: (c.location.y, c.location.x))
        for car in cars:
            car.go_next(commands)
            collided, point = collide(cars)
            if collided:
                return point
            
def solution2():
    cars, commands = data()
    
    while len(cars) > 1:
        cars = sorted(cars, key = lambda c: (c.location.y, c.location.x))
        for car in cars:
            car.go_next(commands)
            collide(cars)
        cars = [car for car in cars if not car.iscollided]
    return cars[0].location 
    
def collide(cars):
    counter = Counter([car.location for car in cars if not car.iscollided])
    point, count = counter.most_common(1)[0]
    if count > 1:
        for car in cars:
            if car.location == point:
                car.iscollided = True
                
    return count > 1, point
        
def data():
    cars = []
    m = {}
    with open('data/input_day13.txt') as f:
        for y, line in enumerate(f):
            for x, v in enumerate(line):
                point = Point(x, y)
                if v in '/-|\+':
                    m[point] = v
                elif v in '^v':
                    m[point] = '|'
                    direction = UP if v == '^' else DOWN
                    cars.append(Car(direction=direction, location=point))
                elif v in '<>':
                    m[point] = '-'
                    direction = LEFT if v == '<' else RIGHT
                    cars.append(Car(direction=direction, location=point))
                else:  # for whitespace
                    continue
    return cars, m