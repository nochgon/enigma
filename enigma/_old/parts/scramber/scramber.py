import copy

from .. import code_map as cm


class Scramber:
    def __init__(self, code_map: cm.CodeMap, step: int = 0,
                 _direct=True) -> None:
        if _direct:
            raise NotImplementedError('private initiator')
        self.__code_map = code_map
        self.__size_scramber = code_map.size
        self.__step = step

    def set_step(self, step: int) -> None:
        self.__step = step

    def add_step(self) -> bool:
        """
        ステップを1つ進める。一周回った場合にTrueを返す
        """
        step_next = self.__step + 1
        self.__step = step_next % self.__size_scramber
        return True if step_next >= self.__size_scramber else False

    def scramble(self, num_input: int) -> int:
        """
        順方向に変換
        """
        num = (num_input + self.__step) % self.__size_scramber
        num = self.__code_map.transfer(num)
        return (num - self.__step) % self.__size_scramber

    def scramble_reverse(self, num_output: int) -> int:
        """
        逆方向に変換
        """
        num = (num_output + self.__step) % self.__size_scramber
        num = self.__code_map.retransfer(num)
        return (num - self.__step) % self.__size_scramber

    def __deepcopy__(self):
        return Scramber(self.__code_map, copy.deepcopy(self.__step))