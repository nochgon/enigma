from typing import Dict


class PlugLink:
    def __init__(self) -> None:
        self.__dict_plug_map: Dict[int, int] = dict()

    def convert(self, num_input: int) -> int:
        if num_input in self.__dict_plug_map:
            return self.__dict_plug_map[num_input]
        else:
            return num_input

    def connect_plug(self, *pair_plugs: int) -> None:
        if len(pair_plugs) != 2:
            raise ValueError(f'指定数が多い: {str(pair_plugs)}')
        if not all([isinstance(e, int) for e in pair_plugs]):
            raise ValueError('指定は数字で行う')

        if pair_plugs[0] in self.__dict_plug_map:
            del self.__dict_plug_map[pair_plugs[0]]
        if pair_plugs[1] in self.__dict_plug_map:
            del self.__dict_plug_map[pair_plugs[1]]

        self.__dict_plug_map.update(
            {pair_plugs[0]: pair_plugs[1],
             pair_plugs[1]: pair_plugs[0]}
        )

    def renew(self) -> None:
        self.__dict_plug_map: Dict[int, int] = dict()
