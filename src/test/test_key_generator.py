import sys
import pathlib

sys.path.append(str(pathlib.Path('.').resolve()))
print(sys.path)

import src.solver as sl
import src.enigma as engm


def test_key_generator(generator: sl.key_generator.KeyGenerator,
                       num_generator: int):
    count = 1
    for ring_key, rotate_key, num_reverse in generator.get_keys():
        print(f'{ring_key}, {rotate_key}, {num_reverse}')
        if count > num_generate:
            break
        else:
            count += 1


encoder = engm.parts.EncoderFactory.create('alphabet')
enigma = engm.EnigmaFactory.create_random('alphabet', 2)
generator = sl.key_generator.KeyGenerator(encoder, enigma, pathlib.Path('.'))

num_generate = 20
test_key_generator(generator, num_generate)
print()
generator.reset()
generator = sl.key_generator.KeyGenerator(encoder, enigma, pathlib.Path('.'))
test_key_generator(generator, num_generate)
