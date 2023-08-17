from enum import IntEnum


class VarcharLength(IntEnum):
    Small = 32
    Middle = 128
    Large = 512
    ExLarge = 2048
    Max = 65535

