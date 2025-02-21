from enum import Enum


class TimeFormat(str, Enum):
    """Допустимые форматы времени со строковыми значениями"""

    HUMAN = "human"
    ISO = "iso"
