from . import encoder as ecd


class EncoderFactory:
    __str_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    __map_command_str = {
        'alphabet': __str_alphabet
    }

    @classmethod
    def create(cls, command: str) -> ecd.Encoder:
        if command in cls.__map_command_str:
            target_chars = cls.__map_command_str[command]
            map_encode = {
                 target_chars[i]: i for i in range(len(target_chars))
            }
            return ecd.Encoder(map_encode)
        else:
            raise ValueError(f'コマンドが不正: {command}')
