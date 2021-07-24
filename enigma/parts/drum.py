from typing import List, Tuple

from . import scramber as scrmb
from . import reflector as rflc


class Drum:
    def __init__(self, scrambers: List[scrmb.Scramber],
                 reflector: rflc.Reflector,
                 positions_scramber: Tuple[int, ...] = None, _direct=True
                 ) -> None:
        if _direct:
            raise NotImplementedError('private initiator')
        if not positions_scramber:
            positions_scramber = tuple([i for i in range(len(scrambers))])

        size_reflector = reflector.size
        if any([scramber != size_reflector for scramber in scrambers]):
            raise ValueError('スクランバーかリフレクターの大きさが一致していない')

        self.__scrambers = scrambers
        self.__len_scrambers = len(scrambers)
        self.__reflector = reflector
        self.arrange_scrambers(*positions_scramber)
        self.__size = size_reflector

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

    def transfer(self, num_input) -> int:
        num_o: int = num_input
        # 変換処理
        for position in self.__positions_scramber:
            num_o = self.__scrambers[position - 1].scramble(num_o)
        num_o = self.__reflector.reflect(num_o)
        for position in reversed(self.__positions_scramber):
            num_o = self.__scrambers[position - 1].scramble_reverse(num_o)

        # scrambers回転処理
        for position in self.__positions_scramber:
            if not self.__scrambers[position - 1].add_step():
                break
        return num_o
