import sys
import pathlib

sys.path.append(str(pathlib.Path.cwd()))

import enigma.parts.scramber as scr

scrmb = scr.Scramber.create(10, 0)
test1 = scrmb.scramble(1)
test2 = scrmb.scramble(2)
test3 = scrmb.scramble(3)
print(f'test1: {test1}\ntest2: {test2}\ntest3: {test3}')
print(f'test1_rev: {scrmb.scramble_reverse(test1)}')
print(f'test2_rev: {scrmb.scramble_reverse(test2)}')
print(f'test3_rev: {scrmb.scramble_reverse(test3)}')

outputs = list()
for i in range(15):
    output = scrmb.scramble(0)
    outputs.append(output)
    print(f'test1(step: {i}): {output}')
    print(f'judge_step: {scrmb.add_step()}')

scrmb.set_step(0)
i = 0
for output in outputs:
    print(f'test1(step: {i}): {scrmb.scramble_reverse(output)}')
    scrmb.add_step()
    i += 1
