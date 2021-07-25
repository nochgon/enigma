from .. import code_map as cm


class Reflector:
    def __init__(self, code_map: cm.CodeMap, _direct=True) -> None:
        if _direct:
            raise NotImplementedError('private initiator')
        if code_map.size % 2 != 0:
            raise ValueError('リフレクターの口は偶数のみ')
        self.__code_map = code_map

    @property
    def size(self) -> int:
        return self.__code_map.size

    def reflect(self, num_input: int) -> int:
        return self.__code_map.transfer(num_input)

    def __deepcopy__(self):
        return Reflector(self.__code_map)
