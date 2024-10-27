from lark import Lark, Transformer

from ttbuilder.common.activity import Activity
from ttbuilder.common.location import Location
from ttbuilder.common.timing_point import TimingPoint
from ttbuilder.common.train_id import TrainId
from ttbuilder.common.ttime import Allowance, TMin, TTime


class TransformTTime(Transformer):
    """Transformer for ttime.lark"""

    # pylint: disable=missing-function-docstring,invalid-name

    def timing_point(self, args):
        location, ttime, allowances, *_ = args
        alw_param = {}
        for x in allowances or []:
            if x.type == Allowance.Type.ENGINEERING:
                alw_param["engineering_allowance"] = TTime.from_tmin(x.time)
            if x.type == Allowance.Type.PATHING:
                alw_param["pathing_allowance"] = TTime.from_tmin(x.time)
            if x.type == Allowance.Type.PERFORMANCE:
                alw_param["performance_allowance"] = TTime.from_tmin(x.time)

        return TimingPoint(location=location, depart=ttime, **alw_param)

    def location(self, args):
        tiploc, platform = args
        return Location(tiploc=tiploc, platform=platform or "")

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

    def allowances(self, args):
        return args

    def eng_allowance(self, args):
        (m,) = args
        return Allowance(m, Allowance.Type.ENGINEERING)

    def path_allowance(self, args):
        (m,) = args
        return Allowance(m, Allowance.Type.PATHING)

    def perf_allowance(self, args):
        (m,) = args
        return Allowance(m, Allowance.Type.PERFORMANCE)

    def train_id(self, args):
        return "".join(args)

    def train_uid(self, args):
        return "".join(args)

    def train_full_id(self, args):
        _id, uid = args
        uid = uid or ""
        return TrainId(_id, uid)

    def activity_type(self, args):
        (atype,) = args
        return getattr(Activity.Type, atype.type, Activity.Type.INVALID)

    def activity(self, args):
        return Activity(*args)


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
