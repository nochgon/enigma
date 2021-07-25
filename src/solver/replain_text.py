import statistics
import collections
from typing import Any, Dict

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

        # 復号
        engm.set_rings(ring_key)
        engm.rotate_scrambers(rotate_key)
        self.__text = engm.execute(text_target)

        # 標本偏差の産出
        counter_char = collections.Counter(self.__text.replace(' ', ''))
        list_count = ([count for count in counter_char.values()] +
                      [0 for i in range(engm.size_encoder - len(counter_char))]
                      )
        self.__stdev = statistics.stdev(list_count)

    @property
    def stdev(self) -> float:
        return self.__stdev

    @property
    def text(self) -> str:
        return self.__text

    def export_result(self) -> Dict[str, Any]:
        return {
            'ring_key': self.__key_ring,
            'rotate_key': self.__key_rotate,
            'reverse_key': self.__key_reverse,
            'replain_text': self.__text,
            'stdev_result': self.__stdev
        }
