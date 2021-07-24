from typing import Tuple, Any

from . import enigma
from . import parts


class EnigmaFactory:
    __map_command_size = {
        'alphabet': 26
    }

    @classmethod
    def create(cls, command: str, len_scrambers: int,
               seeds_scramber: Tuple[Any, ...] = None,
               seed_reflector: Any = None
               ) -> enigma.Enigma:
        if command not in cls.__map_command_size:
            raise ValueError(f'commandが不正: {command}')

        encoder = parts.EncoderFactory.create(command)
        plug = parts.PlugLink.create()
        drum = parts.Drum.create(cls.__map_command_size[command],
                                 len_scrambers,
                                 seeds_scramber=seeds_scramber,
                                 seed_reflector=seed_reflector)
        return enigma.Enigma(drum, plug, encoder)
