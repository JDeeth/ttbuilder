from lark import Lark, Transformer
from ttbuilder.common.ttime import TMin, TTime


class TransformTTime(Transformer):
    """Transformer for ttime.lark"""

    # pylint: disable=missing-function-docstring,invalid-name
    def ttime(self, args):
        hour, stopmode, tmin = args
        return TTime(
            hour * 3600 + tmin.minute * 60 + tmin.second,
            stopmode,
        )

    def HOUR(self, n):
        return int("".join(n))

    def stopmode(self, args):
        (mode,) = args
        return getattr(TTime.StopMode, mode.type, TTime.StopMode.PASSING)

    def tmin(self, args):
        minute, halfminute = args
        return TMin(minute, bool(halfminute))

    def MINUTE(self, n):
        return int("".join(n))

    def HALFMINUTE(self, _):
        return True


class TTimeParser:
    """Parser for TTime/TMin objects"""

    # pylint: disable=too-few-public-methods
    def __init__(self, rule: str = "start"):
        valid_rules = "start tt_time tt_min".split()
        if rule not in valid_rules:
            raise ValueError(f"{rule} must be in {valid_rules}")
        self._parser = Lark.open("ttime.lark", rel_to=__file__, start=rule)

    def parse(self, text):
        """Convert text to TTime/TMin object"""
        tree = self._parser.parse(text)
        return TransformTTime().transform(tree)
