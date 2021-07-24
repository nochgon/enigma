import sys
import pathlib

sys.path.append(str(pathlib.Path.cwd()))

import enigma.parts.scramber as scr


def test_scramble(len_outputs: int, step_start=0, num_input=0,
                  num_ring=0):
    outputs = list()
    scrmb.set_step(step_start)
    scrmb.set_ring(num_ring)
    for i in range(len_outputs):
        output = scrmb.scramble(num_input)
        outputs.append(output)
        print(f'test1(step: {i}): {output}')
        print(f'judge_step: {scrmb.add_step()}')

    print(f'\nnum_input: {num_input}')
    scrmb.set_step(step_start)
    i = 0
    for output in outputs:
        print(f'test_rev(step: {i}): {scrmb.scramble_reverse(output)}')
        scrmb.add_step()
        i += 1


scrmb = scr.Factory.create_random(10, 0)
test1 = scrmb.scramble(1)
test2 = scrmb.scramble(2)
test3 = scrmb.scramble(3)
print(f'test1: {test1}\ntest2: {test2}\ntest3: {test3}')
print(f'test1_rev: {scrmb.scramble_reverse(test1)}')
print(f'test2_rev: {scrmb.scramble_reverse(test2)}')
print(f'test3_rev: {scrmb.scramble_reverse(test3)}')

test_scramble(15, 0)
print()
test_scramble(15, 0, num_ring=1)
