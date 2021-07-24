import sys

sys.path.append('../enigma')

import enigma.reflector as rfl

scrmb = rfl.Reflector.create(10)
test1 = scrmb.scramble(1)
test2 = scrmb.scramble(2)
test3 = scrmb.scramble(3)
print(f'test1: {test1}\ntest2: {test2}\ntest3: {test3}')

for i in range(10):
    print(f'input({i}): {scrmb.scramble(i)}')

for i in range(10000):
    if i % 100 == 0:
        print(f'now {i}')
    rfltr = rfl.Reflector.create(10)
    for j in range(10):
        if j == rfltr.scramble(j):
            raise Exception('同じ値')
