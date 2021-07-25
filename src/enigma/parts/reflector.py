from typing import Any, Dict, List
import random


class Reflector:
    def __init__(self, map_scramble: Dict[int, int], _direct=True) -> None:
        if _direct:
            raise NotImplementedError('private initiator')
        self.__map_scramble: Dict[int, int] = map_scramble

    @classmethod
    def create(cls, size_scramber: int, random_seed: Any = None):
        if size_scramber % 2 != 0:
            raise ValueError(f'size_scramberは偶数のみ: {size_scramber}')
        if random_seed is not None:
            random.seed(random_seed)
        list_input: List[int] = [i for i in range(size_scramber)]
        list_random = random.sample(list_input, len(list_input))
        list_pairs = [(list_random[2 * i], list_random[2 * i + 1])
                      for i in range(size_scramber // 2)]
        map_scramble = dict()
        map_scramble.update({
            pair[0]: pair[1]
            for pair in list_pairs
        })
        map_scramble.update({
            pair[1]: pair[0]
            for pair in list_pairs
        })
        return cls(map_scramble, _direct=False)

    def scramble(self, num_input: int) -> int:
        """
        順方向に変換
        """
        return self.__map_scramble[num_input]

    def __deepcopy__(self):
        return Reflector(self.__map_scramble)
