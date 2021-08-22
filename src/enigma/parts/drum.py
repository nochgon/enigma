from typing import List, Tuple

from . import scramber as scrmb
from . import reflector as rflc


class Drum:
    def __init__(self, scrambers: List[scrmb.Scramber],
                 reflector: rflc.Reflector,
                 positions_scramber: Tuple[int, ...] = None
                 ) -> None:
        size_reflector = reflector.size
        if any([scramber.size != size_reflector for scramber in scrambers]):
            raise ValueError('スクランバーかリフレクターの大きさが一致していない')

        self.__map_scramber = {
            i+1: scramber for i, scramber in enumerate(scrambers)
        }

        if positions_scramber:
            # 指定がある場合はその順番でキューに格納
            self.__list_scrambers = [
                scrambers[position - 1] for position in positions_scramber
            ]
        else:
            # スクランバーの順番指定がない場合はそのままキューに格納
            self.__list_scrambers = scrambers

        self.__len_scrambers = len(scrambers)
        self.__reflector = reflector
        self.__size = size_reflector

    def arrange_scrambers(self, *positions: int) -> None:
        """
        可変長引数で配置する順番にスクランバーを設定する
        """
        if len(positions) > self.__len_scrambers:
            raise ValueError(f'指定個数が違う。(len_positions: {len(positions)})')
        if not any([1 <= position <= self.__len_scrambers
                    for position in positions]):
            raise ValueError(f'ポジション指定が不正: {str(positions)}')
        if len(set(positions)) != len(positions):
            raise ValueError('positionsに重複あり')

        self.__list_scrambers = [
            self.__map_scramber[position] for position in positions
        ]

    def rotate_scrambers(self, *rotations: int) -> None:
        if len(rotations) != self.__len_scrambers:
            raise ValueError(f'指定個数が違う。(len_positions: {len(rotations)})')
        if not any([0 <= rotation < self.__size
                    for rotation in rotations]):
            raise ValueError(f'ポジション指定が不正: {str(rotations)}')

        for i, rotation in enumerate(rotations):
            self.__map_scramber[i + 1].set_step(rotation)

    def set_ring(self, *nums_ring: int) -> None:
        if len(nums_ring) != self.__len_scrambers:
            raise ValueError(f'指定個数が違う。(len_positions: {len(nums_ring)})')
        if not any([0 <= num < self.__size
                    for num in nums_ring]):
            raise ValueError(f'リング指定が不正: {str(nums_ring)}')

        for i, num_ring in enumerate(nums_ring):
            self.__map_scramber[i + 1].set_ring(num_ring)

    def on_reverse(self, position: int) -> None:
        if 1 <= position <= self.__size:
            self.__map_scramber[position].on_reverse()
        else:
            raise ValueError(f'positionが不正: {position}')

    def off_reverse(self, position: int) -> None:
        if 1 <= position <= self.__size:
            self.__map_scramber[position].off_reverse()
        else:
            raise ValueError(f'positionが不正: {position}')

    def transfer(self, num_input) -> int:
        num_o: int = num_input
        # 変換処理
        for scramber in self.__list_scrambers:
            num_o = scramber.scramble(num_o)
        num_o = self.__reflector.reflect(num_o)
        for scramber in reversed(self.__list_scrambers):
            num_o = scramber.scramble_reverse(num_o)

        # scrambers回転処理
        for i in range(len(self.__list_scrambers)):
            if not self.__list_scrambers[i].add_step():
                break
        return num_o

    def __len__(self) -> int:
        return len(self.__list_scrambers)
