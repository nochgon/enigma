from typing import List, Tuple

from . import scramber as scrmb
from . import reflector as rflc


class Drum:
    def __init__(self, scrambers: List[scrmb.Scramber],
                 reflector: rflc.Reflector,
                 positions_scramber: Tuple[int, ...] = None
                 ) -> None:
        if not positions_scramber:
            # スクランバーの順番指定がない場合は(1, 2, 3, ...)
            positions_scramber = tuple([i + 1 for i in range(len(scrambers))])

        size_reflector = reflector.size
        if any([scramber.size != size_reflector for scramber in scrambers]):
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

        for position, rotation in zip(self.__positions_scramber, rotations):
            self.__scrambers[position - 1].set_step(rotation)

    def set_ring(self, *nums_ring: int) -> None:
        if len(nums_ring) != self.__len_scrambers:
            raise ValueError(f'指定個数が違う。(len_positions: {len(nums_ring)})')
        if not any([0 <= num < self.__size
                    for num in nums_ring]):
            raise ValueError(f'リング指定が不正: {str(nums_ring)}')

        for position, num_ring in zip(self.__positions_scramber, nums_ring):
            self.__scrambers[position - 1].set_step(num_ring)

    def on_reverse(self, position: int) -> None:
        if 1 <= position <= self.__size:
            index = self.__positions_scramber[position - 1]
            self.__scrambers[index].on_reverse()
        else:
            raise ValueError(f'positionが不正: {position}')

    def off_reverse(self, position: int) -> None:
        if 1 <= position <= self.__size:
            index = self.__positions_scramber[position - 1]
            self.__scrambers[index].off_reverse()
        else:
            raise ValueError(f'positionが不正: {position}')

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
