import sys
import collections

sys.path.append('../enigma')

import enigma

engm = enigma.EnigmaFactory.create('alphabet', 3, (0, 1, 2, 3, 4), 3)
engm.arrange_scrambers(1, 3, 2)
engm.connect_plug(('B', 'D'), ('C', 'K'), ('X', 'A'))

text = ('that if the british empire and its commitwealth last thousand years\n'
        'they will still say\n'
        'thats was their finest hour')
plain = text.upper()
engm.rotate_scrambers('CAT')
ciphered = engm.execute(plain)
print(f'chiphered:\n{ciphered}')

engm.rotate_scrambers('CAT')
plain_re = engm.execute(ciphered)
print(f'plain_re:\n{plain_re}')

engm.rotate_scrambers('CAT')
key_day = engm.execute('DOGDOG')
print(f'DOGDOG: {key_day}')
