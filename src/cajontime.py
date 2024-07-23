from dataclasses import dataclass


@dataclass
class CajonTime:
    value: int

    @classmethod
    def from_hms(cls, hour: int = 0, minute: int = 0, second: int = 0):
        return cls(value=second + 60 * minute + 3600 * hour)

    @classmethod
    def from_str(cls, text):
        text = text.split(":")
        text.extend(("0", "0", "0"))
        h, m, s, *_ = (int(x) for x in text if x.isdigit())
        return cls.from_hms(h, m, s)
