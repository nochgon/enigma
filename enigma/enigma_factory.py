from typing import Tuple, Any

from . import enigma
from . import parts


class EnigmaFactory:
    __map_command_size = {
        'alphabet': 26
    }

    @classmethod
    def create_random(cls, command: str, len_scrambers: int,
                      seeds_scramber: Tuple[Any, ...] = None,
                      seed_reflector: Any = None
                      ) -> enigma.Enigma:
        if command not in cls.__map_command_size:
            raise ValueError(f'commandが不正: {command}')
        # encoderを先に生成。サイズの情報を持っているため。
        encoder = parts.EncoderFactory.create(command)

        # 乱数シードの指定があるならそれを使って生成
        scrambers = [
            parts.ScramberFactory.create_random(encoder.size, seed)
            for seed in seeds_scramber
        ] if seeds_scramber else [
            parts.ScramberFactory.create_random(encoder.size)
            for i in range(len_scrambers)
        ]
        reflector = parts.ReflectorFactory.create_random(encoder.size,
                                                         seed_reflector)

        drum = parts.Drum(scrambers, reflector)
        plug = parts.PlugLink()
        return enigma.Enigma(drum, plug, encoder)
