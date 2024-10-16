from dataclasses import dataclass


@dataclass(frozen=True)
class TTime:
    """Timetable time - stopping or passing"""

    seconds: int = 0
    passing: bool = False

    @classmethod
    def from_hms(
        cls, hours: int = 0, minutes: int = 0, seconds: int = 0, passing: bool = False
    ):
        """Create time from arbitrary numbers of hours, minutes, and seconds"""
        seconds = 3600 * hours + 60 * minutes + seconds
        return cls(seconds, passing)

    @classmethod
    def from_str(cls, text: str):
        """HH:MM stopping, HH/MM passing, suffix H for +30sec"""
        ends_with_h = text.endswith("H")
        if ends_with_h:
            text = text[:-1]
        passing = "/" in text
        if passing:
            text = text.replace("/", ":")
        text = text.split(":")
        text.extend(("0", "0", "0"))
        h, m, s, *_ = (int(x) for x in text if x.isdigit())
        if ends_with_h:
            s += 30
        return cls.from_hms(h, m, s, passing)

    def __str__(self):
        """To timetable format e.g. 20:45H, 03/20"""
        s = int(self.seconds)
        h = s // 3600
        m = (s // 60) % 60
        s = s % 60
        sep = "/" if self.passing else ":"
        half = "H" if s >= 30 else ""
        return f"{h:02}{sep}{m:02}{half}"

    def __format__(self, spec):
        """Spec MH for minutes+halfminutes, else timetable format"""
        if spec == "MH":
            m = self.seconds // 60
            half = "H" if (self.seconds % 60) >= 30 else ""
            return f"{m}{half}"
        return self.__str__()

    def __bool__(self):
        return self.seconds != 0

    def __eq__(self, other):
        return self.seconds, self.passing == other.seconds, other.passing
