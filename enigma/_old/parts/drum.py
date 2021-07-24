from typing import Any, List, Tuple

from . import scramber as scrmb
from . import reflector as rflc


class Drum:
    def __init__(self, scrambers: List[scrmb.Scramber],
                 reflector: rflc.Reflector, size: int,
                 positions_scramber: Tuple[int, ...] = None, _direct=True
                 ) -> None:
        if _direct:
            raise NotImplementedError('private initiator')
        if not positions_scramber:
            positions_scramber = tuple([i for i in range(len(scrambers))])
        self.__scrambers = scrambers
        self.__len_scrambers = len(scrambers)
        self.__reflector = reflector
        self.arrange_scrambers(*positions_scramber)
        self.__size = size

    @classmethod
    def create(cls, size_scramber: int, len_scrambers: int,
               positions_scramber: Tuple[int, ...] = None,
               seeds_scramber: Tuple[Any, ...] = None,
               seed_reflector: Any = None):
        if seeds_scramber:
            if len(seeds_scramber) < len_scrambers:
                raise ValueError(f'seeds_scramberの長さが短い:'
                                 f' {len(seeds_scramber)}')
            scrambers = [scrmb.Scramber.create(size_scramber,
                                               seeds_scramber[i])
                         for i in range(len_scrambers)]
        else:
            scrambers = [scrmb.Scramber.create(size_scramber)
                         for i in range(len_scrambers)]

        if seed_reflector is None:
            reflector = rflc.Reflector.create(size_scramber)
        else:
            reflector = rflc.Reflector.create(size_scramber, seed_reflector)

        if positions_scramber:
            return cls(scrambers, reflector, size_scramber, positions_scramber,
                       _direct=False)
        else:
            return cls(scrambers, reflector, size_scramber, _direct=False)

    def arrange_scrambers(self, *positions: int) -> None:
        """
        可変長引数で配置する順番にスクランバーの番号を入力する
        """
        if len(positions) > self.__len_scrambers:
            raise ValueError(f'指定個数が違う。(len_positions: {len(positions)})')
        if not any([1 <= position <= self.__len_scrambers
                    for position in positions]):
            raise ValueError(f'ポジション指定が不正: {str(positions)}')
        if len(set(positions)) != len(positions):
            raise ValueError('positionsに重複あり')

        self.__positions_scramber = positions

    def rotate_scrambers(self, *rotations: int) -> None:
        if len(rotations) != self.__len_scrambers:
            raise ValueError(f'指定個数が違う。(len_positions: {len(rotations)})')
        if not any([0 <= rotation < self.__size
                    for rotation in rotations]):
            raise ValueError(f'ポジション指定が不正: {str(rotations)}')

        i_rotate = 0
        for position in self.__positions_scramber:
            self.__scrambers[position - 1].set_step(rotations[i_rotate])
            i_rotate += 1

    def translate(self, num_input) -> int:
        num_o: int = num_input
        # 変換処理
        for position in self.__positions_scramber:
            num_o = self.__scrambers[position - 1].scramble(num_o)
        num_o = self.__reflector.scramble(num_o)
        for position in reversed(self.__positions_scramber):
            num_o = self.__scrambers[position - 1].scramble_reverse(num_o)

        # scrambers回転処理
        for position in self.__positions_scramber:
            if not self.__scrambers[position - 1].add_step():
                break
        return num_o
