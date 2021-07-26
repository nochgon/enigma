import sys
import pathlib

sys.path.append(str(pathlib.Path('./src').resolve()))

import enigma


def test_enigma(engm: enigma.Enigma, text_target: str, rotate_key: str):
    engm.rotate_scrambers(rotate_key)
    text_cipherd = engm.execute(text_target.upper())
    print(f'cipherd:\n{text_cipherd}\n')
    engm.rotate_scrambers(rotate_key)
    text_replain = engm.execute(text_cipherd)
    print(f'replain:\n{text_replain}')


alphabets_sorted = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

str_scramber1 = 'ajdk siru xblh wtmc qgzn pyfv oe'.replace(' ', '').upper()
str_scramber2 = 'ekmf lgdq vznt owyh xusp aibr cj'.replace(' ', '').upper()
str_scramber3 = 'bdfh jlcp rtxv znye iwga kmus qo'.replace(' ', '').upper()
str_reflector = 'yruh qsld pxng okmi ebfz cwvj at'.replace(' ', '').upper()

maps_str_scramber = [
    {
       str_in: str_out
       for str_in, str_out in zip(alphabets_sorted, str_scramber)
    }
    for str_scramber in (str_scramber1, str_scramber2, str_scramber3)
]
map_str_reflector = {
    str_in: str_out for str_in, str_out in zip(alphabets_sorted, str_reflector)
}

engm = enigma.EnigmaFactory.create('alphabet', maps_str_scramber,
                                   map_str_reflector)
engm.set_rings('CAT')
engm.arrange_scrambers(2, 1, 3)
engm.on_reverse(3)

text = ('that if the british empire and its commitwealth last thousand years\n'
        'they will still say\n'
        'thats was their finest hour')

test_enigma(engm, text, 'AAA')
