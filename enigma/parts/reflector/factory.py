from typing import Any, Dict

from . import reflector as rfl
from .. import code_map as cm
from .. import encoder as ec


class Factory:
    @classmethod
    def create(cls, map_char_reflector: Dict[str, str], encoder: ec.Encoder
               ) -> rfl.Reflector:
        map_code = {encoder.encode(char_i): encoder.encode(char_o)
                    for char_i, char_o in map_char_reflector.items()}
        code_map = cm.Factory.create(map_code)
        return rfl.Reflector(code_map, _direct=False)

    @classmethod
    def create_random(cls, size, random_seed: Any = None) -> rfl.Reflector:
        code_map = cm.Factory.create_paired_random(size, random_seed)
        return rfl.Reflector(code_map, _direct=False)
