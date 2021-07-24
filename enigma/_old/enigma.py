from typing import Tuple

from . import parts


class Enigma:
    def __init__(self, drum: parts.Drum, plug_link: parts.PlugLink,
                 encoder: parts.Encoder) -> None:
        self.__drum = drum
        self.__plug_link = plug_link
        self.__encoder = encoder

    def execute(self, text: str) -> str:
        rsl_text = ''
        for char in text:
            if self.__encoder.is_pass(char):
                rsl_text += char
                continue
            num = self.__encoder.encode(char)
            num = self.__plug_link.convert(num)
            num = self.__drum.translate(num)
            num = self.__plug_link.convert(num)
            rsl_text += self.__encoder.decode(num)
        return rsl_text

    def arrange_scrambers(self, *positions: int) -> None:
        self.__drum.arrange_scrambers(*positions)

    def rotate_scrambers(self, rotate_key: str) -> None:
        rotations = [self.__encoder.encode(char) for char in rotate_key]
        self.__drum.rotate_scrambers(*rotations)

    def connect_plug(self, *pair_plugs: Tuple[str, str]) -> None:
        pairs_int = [(self.__encoder.encode(pair[0]),
                      self.__encoder.encode(pair[1]))
                     for pair in pair_plugs]
        self.__plug_link.connect_plug(*pairs_int)
