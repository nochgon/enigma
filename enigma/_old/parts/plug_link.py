from typing import Dict, Tuple


class PlugLink:
    def __init__(self, dict_plug_map: Dict[int, int], _direct=True) -> None:
        if _direct:
            raise NotImplementedError('private initiator')
        self.__dict_plug_map = dict_plug_map

    @classmethod
    def create(cls, *pairs_plugs: Tuple[int, int]):
        rsl = cls(dict(), _direct=False)
        for pair in pairs_plugs:
            rsl.connect_plug(pair)
        return rsl

    def convert(self, num_input: int) -> int:
        if num_input in self.__dict_plug_map:
            return self.__dict_plug_map[num_input]
        else:
            return num_input

    def connect_plug(self, *pair_plugs: Tuple[int, int]) -> None:
        for pair in pair_plugs:
            if len(pair) != 2:
                raise ValueError(f'指定数が多い: {pair}')
        if not all([isinstance(t, int) for e in pair_plugs for t in e]):
            raise ValueError('指定は数字で行う')
        self.__dict_plug_map.update(
            {pair_plugs[0]: pair_plugs[1],
             pair_plugs[1]: pair_plugs[0]}
        )
