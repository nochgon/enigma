import random
from typing import Dict, List


class Scramber:
    def __init__(self, size_scramber: int, map_scramble: Dict[int, int],
                 step: int, _direct=True) -> None:
        if _direct:
            raise NotImplementedError('private initiator')
        self.__size_scramber: int = size_scramber
        self.__map_scramble: Dict[int, int] = map_scramble
        iter_map_scramble = self.__map_scramble.items()
        self.__map_scramble_reverse: Dict[int, int] = {o: i for i, o
                                                       in iter_map_scramble}
        self.__step: int = step

    @classmethod
    def create(cls, size_scramber: int, random_seed: int = None):
        if random_seed is not None:
            random.seed(random_seed)
        list_input: List[int] = [i for i in range(size_scramber)]
        list_output: List[int] = random.sample(list_input, size_scramber)
        map_scramble: Dict[int, int] = {list_input[i]: list_output[i]
                                        for i in range(size_scramber)}
        return cls(size_scramber, map_scramble, 0, _direct=False)

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
        num = self.__map_scramble[num]
        return (num - self.__step) % self.__size_scramber

    def scramble_reverse(self, num_output: int) -> int:
        """
        逆方向に変換
        """
        num = (num_output + self.__step) % self.__size_scramber
        num = self.__map_scramble_reverse[num]
        return (num - self.__step) % self.__size_scramber

    def __deepcopy__(self):
        return Scramber(self.__size_scramber, self.__map_scramble, self.__step)
