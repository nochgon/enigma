from typing import Deque, List, Optional, Tuple
import pathlib
import csv
import collections

from .. import enigma
from . import replain_text as rt


class Solver:
    __dict_command_sorted = {
        'alphabet': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    }
    __header = (
        'index', 'ring_key', 'rotate_key', 'reverse_key',
        'stdev', 'text_replain'
    )
    __list_keys_result = [
        'ring_key', 'rotate_key', 'reverse_key', 'stdev_result', 'replain_text'
    ]

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
                ) -> rt.ReplainText:
        # サーチ結果はキューに格納し、終了時にcsvへ出力
        deque_result: Deque[rt.ReplainText] = collections.deque()

        # サーチ実行
        index = 1
        text_replain_result: Optional[rt.ReplainText] = None
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
                    result = rt.ReplainText(text_target, self.__enigma,
                                            ring_key, rotate_key, num_reverse)
                    deque_result.append(result)
                    index += 1

                    # 標本偏差が最大の翻訳文をキープ
                    if (not text_replain_result or
                       text_replain_result.stdev < result.stdev):
                        text_replain_result = result

                    # csv出力

                    if limit_num and limit_num <= index:
                        self.__export_to_csv(deque_result)
                        return text_replain_result

        if not text_replain_result:
            raise ValueError()
        self.__export_to_csv(deque_result)
        return text_replain_result

    def __export_to_csv(self, deque_replain_text: Deque[rt.ReplainText]
                        ) -> None:
        with open(self.__path_result, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.__header)
            index = 1
            while len(deque_replain_text):
                target = deque_replain_text.popleft()
                result_dict = target.export_result()
                result_list = [result_dict[key]
                               for key in self.__list_keys_result]
                writer.writerow([index] + result_list)
                index += 1
