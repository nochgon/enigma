from typing import Deque, List, Optional, Tuple
import pathlib
import csv
import collections
import statistics

from .. import enigma


class Solver:
    __dict_command_sorted = {
        'alphabet': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    }
    __header = (
        'index', 'ring_key', 'rotate_key', 'reverse_key',
        'text_replain', 'stdev_str'
    )

    def __init__(self, command: str, strs_scramber: List[str],
                 str_reflector: str, positions_scramber: Tuple[int, ...],
                 folder_result: pathlib.Path, name_file: str) -> None:
        self.__path_result = folder_result / f'{name_file}.csv'

        # バリデーション
        if command not in self.__dict_command_sorted:
            raise ValueError(f'コマンドが不正: {command}')

        str_sorted = self.__dict_command_sorted[command]
        maps_str_scramber = [
            {
                str_in: str_out
                for str_in, str_out
                in zip(str_sorted, str_scramber.replace(' ', '').upper())
            }
            for str_scramber in strs_scramber
        ]
        map_str_reflector = {
            str_in: str_out
            for str_in, str_out
            in zip(str_sorted, str_reflector.replace(' ', '').upper())
        }
        encoder = enigma.parts.EncoderFactory.create(command)
        scrambers = [
            enigma.parts.ScramberFactory.create(map_str_scramber, encoder)
            for map_str_scramber in maps_str_scramber
        ]
        reflector = enigma.parts.ReflectorFactory.create(map_str_reflector,
                                                         encoder)
        drum = enigma.parts.Drum(scrambers, reflector)
        plug_link = enigma.parts.PlugLink()
        self.__enigma = enigma.Enigma(drum, plug_link, encoder)
        self.__enigma.arrange_scrambers(*positions_scramber)

        # executeで利用するため、メンバーに追加
        self.__encoder = encoder

    def execute(self, text_target: str, limit_num: Optional[int] = None
                ) -> Tuple[str, float]:
        # サーチ条件をキューに格納
        deque_condition: Deque[Tuple[str, str, int]] = collections.deque()
        for num_ring_key in range(pow(self.__encoder.size,
                                      self.__enigma.len_drum - 1
                                      )):
            ring_key = ''
            for rank in reversed(range(self.__enigma.len_drum - 1)):
                num = num_ring_key // pow(self.__encoder.size, rank)
                ring_key += self.__encoder.decode(num)
                num_ring_key -= num * pow(self.__encoder.size, rank)
            for num_rotate_key in range(pow(self.__encoder.size,
                                            self.__enigma.len_drum
                                            )):
                rotate_key = ''
                for rank in reversed(range(self.__enigma.len_drum)):
                    num = num_rotate_key // pow(self.__encoder.size, rank)
                    rotate_key += self.__encoder.decode(num)
                    num_rotate_key -= num * pow(self.__encoder.size, rank)
                for num_reverse in range(pow(2, self.__enigma.len_drum)):
                    deque_condition.append((ring_key, rotate_key, num_reverse))

        # 回数制限がある場合はキューを短くする
        if limit_num:
            deque_old = deque_condition
            deque_condition = collections.deque()
            for i in range(limit_num):
                deque_condition.append(deque_old.popleft())

        # サーチ実行
        index = 1
        with open(self.__path_result, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.__header)
            stdev_max = 0
            text_replain_result = ''
            while len(deque_condition):
                ring_key, rotate_key, num_reverse = deque_condition.popleft()

                # 回転方向の設定
                for rank in range(self.__enigma.len_drum):
                    if num_reverse % pow(2, rank) == 1:
                        self.__enigma.on_reverse(rank + 1)
                    else:
                        self.__enigma.off_reverse(rank + 1)

                self.__enigma.set_rings(ring_key)
                self.__enigma.rotate_scrambers(rotate_key)
                text_replain = self.__enigma.execute(text_target)

                counter_char = collections.Counter(text_replain.replace(' ',
                                                                        ''))
                list_count = ([count for count in counter_char.values()] +
                              [0 for i in range(self.__encoder.size -
                                                len(counter_char))])
                stdev_result = statistics.stdev(list_count)

                # csv出力
                writer.writerow((
                    index, ring_key, rotate_key, format(num_reverse, 'b'),
                    text_replain, stdev_result
                ))
                index += 1

                # 不偏分散が最大の翻訳文をキープ
                if stdev_max >= stdev_result:
                    text_replain_result = text_replain
                    stdev_max = stdev_result

        return (text_replain_result, stdev_max)
