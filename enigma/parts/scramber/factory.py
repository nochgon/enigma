from typing import Dict, Any

from . import scramber as srb
from .. import encoder as ec
from .. import code_map as cm


class Factory:
    @classmethod
    def create(cls, map_char_reflector: Dict[str, str], encoder: ec.Encoder
               ) -> srb.Scramber:
        map_code = {encoder.encode(char_i): encoder.encode(char_o)
                    for char_i, char_o in map_char_reflector.items()}
        code_map = cm.Factory.create(map_code)
        return srb.Scramber(code_map, _direct=False)

    @classmethod
    def create_random(cls, size: int, random_seed: Any = None) -> srb.Scramber:
        code_map = cm.Factory.create_random(size, random_seed)
        return srb.Scramber(code_map, _direct=False)
