from typing import Dict


class Encoder:
    def __init__(self, map_char_int: Dict[str, int]) -> None:
        self.__map_encode = map_char_int
        self.__map_decode = {
            i: c for c, i in map_char_int.items()
        }

    @property
    def size(self) -> int:
        return len(self.__map_encode)

    def encode(self, char_input: str) -> int:
        if char_input in self.__map_encode:
            return self.__map_encode[char_input]
        else:
            raise ValueError(f'char_inputが不正: {char_input}')

    def decode(self, int_input: int) -> str:
        if int_input in self.__map_decode:
            return self.__map_decode[int_input]
        else:
            raise ValueError(f'int_inputが不正: {int_input}')

    def is_pass(self, char: str) -> bool:
        if char in self.__map_encode:
            return False
        else:
            return True
