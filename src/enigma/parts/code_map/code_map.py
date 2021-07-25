from typing import Dict


class CodeMap:
    def __init__(self, code_map: Dict[int, int]) -> None:
        self.__trans_map = code_map
        self.__retrans_map = {i_out: i_in for i_in, i_out in code_map.items()}

    @property
    def size(self) -> int:
        return len(self.__trans_map)

    def transfer(self, code: int) -> int:
        return self.__trans_map[code]

    def retransfer(self, code: int) -> int:
        return self.__retrans_map[code]
