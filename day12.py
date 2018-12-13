INIT_STATE = "###.......##....#.#.#..###.##..##.....#....#.#.....##.###...###.#...###.###.#.###...#.####.##.#....#"
RULES = r"""..... => .
#..## => .
..### => #
..#.# => #
.#.#. => .
####. => .
##.## => #
#.... => .
#...# => .
...## => .
##..# => .
.###. => #
##### => #
#.#.. => #
.##.. => #
.#.## => .
...#. => #
#.##. => #
..#.. => #
##... => #
....# => .
###.# => #
#..#. => #
#.### => #
##.#. => .
###.. => #
.#### => .
.#... => #
..##. => .
.##.# => .
#.#.# => #
.#..# => ."""


def build_rules():
    return dict([line.split(r' => ') for line in RULES.splitlines()])

def init_state(config = INIT_STATE):
    return {i for i, v in enumerate(config) if v == '#'}

def get_rule(pos, states):
    get = lambda i : '#' if i in states else '.'
    return ''.join([get(i) for i in (pos - 2, pos - 1, pos, pos + 1, pos + 2)])

def evolve(states, rules):
    min_v = min(states) - 2
    max_v = max(states) + 2
    new_state = set()
    for pos in range(min_v, max_v + 1):
       key = get_rule(pos, states)
       nxt_value = rules.get(key, '.')
       if nxt_value == '#':
           new_state.add(pos)
           
    return new_state   
    
def solution1():
    rules = build_rules()
    state = init_state()

    for _ in range(20):
       state = evolve(state, rules)
        
    return sum(state)


# after certain iteration it gets stable and each iteration will add fixed number
def solution2():
    rules = build_rules()
    state = init_state()

    for i in range(1, 1001):
        state = evolve(state, rules)
        print(f'generation {i}, sum {sum(state)}, min value {min(state)}')
        