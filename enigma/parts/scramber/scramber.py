import copy

from .. import code_map as cm


class Scramber:
    def __init__(self, code_map: cm.CodeMap, step: int = 0,
                 num_ring: int = 0, is_reverse: bool = False, _direct=True
                 ) -> None:
        if _direct:
            raise NotImplementedError('private initiator')
        self.__code_map = code_map
        self.__step = step
        self.__num_ring = num_ring
        self.__step_move = -1 if is_reverse else 1

    @property
    def size(self) -> int:
        return self.__code_map.size

    def set_step(self, step: int) -> None:
        self.__step = step

    def set_ring(self, num_ring: int) -> None:
        self.__num_ring = num_ring

    def on_reverse(self) -> None:
        self.__step_move = -1

    def off_reverse(self) -> None:
        self.__step_move = 1

    def add_step(self) -> bool:
        """
        ステップを1つ進める。一周回った場合にTrueを返す
        """
        step_next = self.__step + self.__step_move
        self.__step = step_next % self.__code_map.size
        return (True if self.__step == self.__num_ring else False)

    def scramble(self, num_input: int) -> int:
        """
        順方向に変換
        """
        num = (num_input - self.__step) % self.__code_map.size
        num = self.__code_map.transfer(num)
        return (num + self.__step) % self.__code_map.size

    def scramble_reverse(self, num_output: int) -> int:
        """
        逆方向に変換
        """
        num = (num_output - self.__step) % self.__code_map.size
        num = self.__code_map.retransfer(num)
        return (num + self.__step) % self.__code_map.size

    def __deepcopy__(self):
        return Scramber(self.__code_map, copy.deepcopy(self.__step))
