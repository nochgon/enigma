import sys
import pathlib
from typing import List

sys.path.append(str(pathlib.Path.cwd()))

import enigma.parts as parts


def test_drum(drum: parts.Drum, rotations_start: List[int],
              num_test: int, num_input: int = 0):
    drum.rotate_scrambers(*rotations_start)
    outputs = list()
    for i in range(num_test):
        output = drum.transfer(num_input)
        outputs.append(output)
        print(f'time({i}): {output}')

    print(f'\nnum_input: {num_input}')
    drum.rotate_scrambers(*rotations_start)
    for i, output in enumerate(outputs):
        print(f'time({i}): {drum_test.transfer(output)}')


size = 6
scrambers = [
    parts.ScramberFactory.create_random(size, 'scramber') for i in range(3)
]
reflector = parts.ReflectorFactory.create_random(size, 'reflect')
drum_test = parts.Drum(scrambers, reflector)

drum_test.arrange_scrambers(1, 3, 2)
test_drum(drum_test, [0, 0, 0], 10)
