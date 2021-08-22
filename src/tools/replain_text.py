import statistics
import collections
from typing import Any, Deque, Dict

from .. import enigma


class ReplainText:
    def __init__(self, text_target: str, engm: enigma.Enigma, ring_key: str,
                 rotate_key: str, num_reverse: int) -> None:
        # キー設定の保管
        self.__key_ring = ring_key
        self.__key_rotate = rotate_key
        self.__key_reverse = format(num_reverse, 'b').zfill(engm.len_drum)

        # 回転方向の設定
        for rank in range(engm.len_drum):
            if num_reverse % pow(2, rank) == 1:
                engm.on_reverse(rank + 1)
                num_reverse -= pow(2, rank)
            else:
                engm.off_reverse(rank + 1)

        # 結果の保管場所を確保
        self.__deque_chars_result: Deque[str] = collections.deque()
        dict_char_count: Dict[str, int] = dict()

        # 復号とサンプリング
        engm.set_rings(ring_key)
        engm.rotate_scrambers(rotate_key)
        for char_input in text_target:
            char_output = engm.transfer(char_input)
            self.__deque_chars_result.append(char_output)

            if char_output in dict_char_count:
                dict_char_count[char_output] += 1
            else:
                dict_char_count[char_output] = 1

        # 標本偏差の産出
        list_count = (
            [count for count in dict_char_count.values()] +
            [0 for i in range(engm.size_encoder - len(dict_char_count))]
        )
        self.__stdev = statistics.stdev(list_count)

    @property
    def stdev(self) -> float:
        return self.__stdev

    @property
    def text(self) -> str:
        text_result = ''
        deque_new: Deque[str] = collections.deque()
        while(self.__deque_chars_result):
            char = self.__deque_chars_result.popleft()
            text_result += char
            deque_new.append(char)
        self.__deque_chars_result = deque_new
        return text_result

    def export_result(self) -> Dict[str, Any]:
        return {
            'ring_key': self.__key_ring,
            'rotate_key': self.__key_rotate,
            'reverse_key': self.__key_reverse,
            'replain_text': self.text,
            'stdev_result': self.__stdev
        }
