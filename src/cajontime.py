from dataclasses import dataclass


@dataclass(frozen=True)
class CajonTime:
    seconds: int = 0

    @classmethod
    def from_hms(cls, hours: int = 0, minutes: int = 0, seconds: int = 0):
        return cls(seconds=seconds + 60 * minutes + 3600 * hours)

    @classmethod
    def from_str(cls, text):
        text = text.split(":")
        text.extend(("0", "0", "0"))
        h, m, s, *_ = (int(x) for x in text if x.isdigit())
        return cls.from_hms(h, m, s)
