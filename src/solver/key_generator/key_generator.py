import pathlib
import json
from typing import Tuple, Generator

from ... import enigma


class KeyGenerator:
    __name_file_save = 'save_data_KeyGenerator.json'

    def __init__(self, encoder: enigma.parts.Encoder, engm: enigma.Enigma,
                 folder_save: pathlib.Path) -> None:
        self.__encoder = encoder
        self.__enigma = engm

        self.__path_save = folder_save / self.__name_file_save
        if self.__path_save.exists():
            with open(self.__path_save) as f:
                dict_last_keys = json.load(f)
                self.__num_ring_key = dict_last_keys['num_ring_key']
                self.__num_rotate_key = dict_last_keys['num_rotate_key']
                self.__num_reverse = dict_last_keys['num_reverse']
                self.__time_execute = dict_last_keys['time_execute']
        else:
            self.__num_ring_key = 0
            self.__num_rotate_key = 0
            self.__num_reverse = 0
            self.__time_execute = 0

    @property
    def time_execute(self) -> int:
        return self.__time_execute

    def get_keys(self) -> Generator[Tuple[str, str, int], None, None]:
        """
        返り値: (ring_key, rotate_key, num_reverse)
        """
        # 各キーの最大数
        max_num_ring_key = pow(self.__encoder.size, self.__enigma.len_drum - 1)
        max_num_rotate_key = pow(self.__encoder.size, self.__enigma.len_drum)
        max_num_reverse = pow(2, self.__enigma.len_drum)

        while self.__num_ring_key <= max_num_ring_key:
            # ring_key生成
            num_ring_key = self.__num_ring_key
            ring_key = ''
            for rank in reversed(range(self.__enigma.len_drum - 1)):
                num = num_ring_key // pow(self.__encoder.size, rank)
                ring_key += self.__encoder.decode(num)
                num_ring_key -= num * pow(self.__encoder.size, rank)

            while self.__num_rotate_key <= max_num_rotate_key:
                # rotate_key生成
                rotate_key = ''
                num_rotate_key = self.__num_rotate_key
                for rank in reversed(range(self.__enigma.len_drum)):
                    num = num_rotate_key // pow(self.__encoder.size, rank)
                    rotate_key += self.__encoder.decode(num)
                    num_rotate_key -= num * pow(self.__encoder.size, rank)

                while self.__num_reverse <= max_num_reverse:
                    self.__time_execute += 1
                    yield (ring_key, rotate_key, self.__num_reverse)
                    self.__num_reverse += 1
                self.__num_reverse = 0
                self.__num_rotate_key += 1
            self.__num_rotate_key = 0
            self.__num_ring_key += 1

    def save(self) -> None:
        with open(self.__path_save, 'w') as f:
            json.dump({
                'num_ring_key': self.__num_ring_key,
                'num_rotate_key': self.__num_rotate_key,
                'num_reverse': self.__num_reverse,
                'time_execute': self.__time_execute
            }, f, indent=4)

    def reset(self) -> None:
        if self.__path_save.exists:
            self.__path_save.unlink()
