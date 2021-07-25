import random
from typing import Any, Dict

from . import code_map as cm


class Factory:
    @classmethod
    def create(cls, map_code: Dict[int, int]) -> cm.CodeMap:
        return cm.CodeMap(map_code)

    @classmethod
    def create_random(cls, size: int, random_seed: Any = None,
                      can_self_return: bool = True
                      ) -> cm.CodeMap:
        if random_seed is not None:
            random.seed(random_seed)

        list_output = random.sample([i for i in range(size)], size)
        while (not can_self_return
               and any([i == list_output[i] for i in range(size)])):
            for i in range(size):
                if i == list_output[i]:
                    n_old = list_output[i]
                    i_target = random.choice(list_output)
                    list_output[i] = list_output[i_target]
                    list_output[i_target] = n_old

        map_code = {i: list_output[i] for i in range(size)}
        return cm.CodeMap(map_code)

    @classmethod
    def create_paired_random(cls, size: int, random_seed: Any = None
                             ) -> cm.CodeMap:
        if size % 2 != 0:
            raise ValueError(f'sizeは偶数のみ size={size}')
        if random_seed is not None:
            random.seed(random_seed)

        nums_random = random.sample([i for i in range(size)], size)
        map_num = {nums_random[2 * i]: nums_random[2 * i + 1]
                   for i in range(size // 2)}
        map_num.update({num_o: num_i for num_i, num_o in map_num.items()})
        return cm.CodeMap(map_num)
