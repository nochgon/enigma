import sys
import pathlib

sys.path.append(str(pathlib.Path.cwd()))

import enigma.parts as parts


drum_test = parts.Drum.create(10, 3, (1, 3, 2), (1, 2, 3), 'reflect')
outputs = list()
for i in range(10):
    output = drum_test.translate(0)
    outputs.append(output)
    print(f'time({i}): {output}')

print()
drum_test.rotate_scrambers(0, 0, 0)
i = 0
for output in outputs:
    print(f'time({i}): {drum_test.translate(output)}')
    i += 1
