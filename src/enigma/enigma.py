from . import parts


class Enigma:
    def __init__(self, drum: parts.Drum, plug_link: parts.PlugLink,
                 encoder: parts.Encoder) -> None:
        self.__drum = drum
        self.__plug_link = plug_link
        self.__encoder = encoder

    @property
    def len_drum(self) -> int:
        return len(self.__drum)

    @property
    def size_encoder(self) -> int:
        return self.__encoder.size

    def execute(self, text: str) -> str:
        """
        文字列を翻訳する。
        """
        rsl_text = ''
        for char in text:
            if self.__encoder.is_pass(char):
                rsl_text += char
                continue
            num = self.__encoder.encode(char)
            num = self.__plug_link.convert(num)
            num = self.__drum.transfer(num)
            num = self.__plug_link.convert(num)
            rsl_text += self.__encoder.decode(num)
        return rsl_text

    def transfer(self, char: str) -> str:
        """
        一文字だけを変換する
        """
        num = self.__encoder.encode(char)
        num = self.__encoder.encode(char)
        num = self.__plug_link.convert(num)
        num = self.__drum.transfer(num)
        num = self.__plug_link.convert(num)
        return self.__encoder.decode(num)

    def arrange_scrambers(self, *positions: int) -> None:
        self.__drum.arrange_scrambers(*positions)

    def rotate_scrambers(self, rotate_key: str) -> None:
        rotations = [self.__encoder.encode(char) for char in rotate_key]
        self.__drum.rotate_scrambers(*rotations)

    def set_rings(self, ring_key: str) -> None:
        num_rings = [self.__encoder.encode(char) for char in ring_key]
        self.__drum.set_ring(*num_rings)

    def on_reverse(self, position: int) -> None:
        self.__drum.on_reverse(position)

    def off_reverse(self, position: int) -> None:
        self.__drum.off_reverse(position)

    def connect_plug(self, *pair_plugs: str) -> None:
        if len(pair_plugs) != 2:
            raise ValueError(f'pair_plugsの個数が不正: {len(pair_plugs)}')
        if any([not isinstance(char, str) for char in pair_plugs]):
            raise ValueError(f'プラグの指定は文字列で行う')
        if any([len(char) != 1 for char in pair_plugs]):
            raise ValueError(f'プラグの指定は一文字で行う')
        pair_num = [self.__encoder.encode(char) for char in pair_plugs]
        self.__plug_link.connect_plug(*pair_num)
