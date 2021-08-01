from typing import Deque, List, Optional, Tuple
import pathlib
import csv
import collections
import pickle

from .. import enigma
from . import replain_text as rt
from . import key_generator as kg


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
    __name_pickle_replain = 'replain.pickle'

    def __init__(self, command: str, strs_scramber: List[str],
                 str_reflector: str, positions_scramber: Tuple[int, ...],
                 folder_result: pathlib.Path, name_file: str) -> None:
        self.__path_pickle_replain = folder_result / self.__name_pickle_replain

        # バリデーション
        if command not in self.__dict_command_sorted:
            raise ValueError(f'コマンドが不正: {command}')

        # Enigma生成
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

        # KeyGenerator生成
        self.__key_generator = kg.KeyGenerator(self.__encoder, self.__enigma,
                                               folder_result)
        self.__len_record = self.__key_generator.time_execute

        # 結果出力先のCSVファイルの準備
        self.__path_result = folder_result / f'{name_file}.csv'
        if not self.__path_result.exists():
            with open(self.__path_result, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.__header)

    def execute(self, text_target: str, limit_num: Optional[int] = None
                ) -> rt.ReplainText:
        # サーチ結果はキューに格納し、終了時にcsvへ出力
        deque_result: Deque[rt.ReplainText] = collections.deque()

        # 標本偏差が最大の翻訳文を取得。(初回はNone)
        text_replain_result: Optional[rt.ReplainText] = None
        if self.__path_pickle_replain.exists():
            with open(self.__path_pickle_replain, 'rb') as f:
                text_replain_result = pickle.load(f)

        # サーチ実行
        self.__len_record = self.__key_generator.time_execute
        count = 1
        generator = self.__key_generator.get_keys()
        for ring_key, rotate_key, num_reverse in generator:
            result = rt.ReplainText(text_target, self.__enigma,
                                    ring_key, rotate_key, num_reverse)
            deque_result.append(result)
            count += 1

            # 標本偏差が最大の翻訳文をキープ
            if (not text_replain_result or
               text_replain_result.stdev < result.stdev):
                text_replain_result = result

            # 指定された検索回数が終わったら中断
            if limit_num and limit_num <= count:
                self.__export_to_csv(deque_result)
                self.__key_generator.save()
                with open(self.__path_pickle_replain, 'wb') as f:
                    pickle.dump(text_replain_result, f)
                return text_replain_result

        if not text_replain_result:
            raise ValueError()
        self.__export_to_csv(deque_result)
        self.__key_generator.reset()
        print('\n***全検索が完了***')
        return text_replain_result

    def __export_to_csv(self, deque_replain_text: Deque[rt.ReplainText]
                        ) -> None:
        with open(self.__path_result, 'a', newline='') as f:
            writer = csv.writer(f)
            index = self.__len_record + 1
            while len(deque_replain_text):
                target = deque_replain_text.popleft()
                result_dict = target.export_result()
                result_list = [result_dict[key]
                               for key in self.__list_keys_result]
                writer.writerow([index] + result_list)
                index += 1
