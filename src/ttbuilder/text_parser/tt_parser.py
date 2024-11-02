from lark import Lark, Transformer

from ttbuilder.common.location import Location
from ttbuilder.common.timing_point import TimingPoint
from ttbuilder.common.train_id import TrainId
from ttbuilder.common import activity, allowance, ttime


class TransformTT(Transformer):
    """Transformer for timetable.lark"""

    # pylint: disable=missing-function-docstring,invalid-name

    def timing_point(self, args):
        location, tt, allowances, activities = args
        allowances = [x for x in allowances or [] if x.time]
        tt = ttime.TTime(tt.seconds, tt.stop_mode)

        return TimingPoint(
            location=location,
            depart=tt,
            activities=list(activities or []),
            allowances=allowances,
        )

    def location(self, args):
        tiploc, platform = args
        return Location(tiploc=tiploc, platform=platform or "")

    def ttime(self, args):
        hour, stopmode, tmin = args
        return ttime.TTime(
            hour * 3600 + tmin.seconds,
            stopmode,
        )

    def HOUR(self, n):
        return int("".join(n))

    def stopmode(self, args):
        (mode,) = args
        return getattr(ttime.StopMode, mode.type, ttime.StopMode.NOT_DEFINED)

    def tmin(self, args):
        minute, halfminute = args
        return ttime.TTime.from_hms(
            minutes=int(minute), seconds=30 if halfminute else 0
        )

    def MINUTE(self, n):
        return int("".join(n))

    def HALFMINUTE(self, _):
        return True

    def allowances(self, args):
        return args

    def eng_allowance(self, args):
        (m,) = args
        return allowance.Engineering(m)

    def path_allowance(self, args):
        (m,) = args
        return allowance.Pathing(m)

    def perf_allowance(self, args):
        (m,) = args
        return allowance.Performance(m)

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
        return getattr(activity.Type, atype.type, activity.Type.INVALID)

    def activity(self, args):
        atype, train_id = args
        return activity.Activity(associated_train_id=train_id, activity_type=atype)

    def activities(self, args):
        return list(args)


class TTParser:
    """Parser for timetable elements"""

    def __init__(self):
        self._parsers = {}

    def _get_parser(self, rule):
        def _make_parser(rule):
            return Lark.open(
                grammar_filename="timetable.lark",
                rel_to=__file__,
                start=rule,
                parser="lalr",
                transformer=TransformTT(),
            )

        return self._parsers.setdefault(rule, _make_parser(rule))

    def _parse(self, text, rule):
        return self._get_parser(rule).parse(text)

    def parse_train_full_id(self, text):
        """Parse for train ID[/UID]"""
        return self._parse(text, "train_full_id")

    def parse_timing_point(self, text):
        """Parse for timing point line"""
        return self._parse(text, "timing_point")

    def parse_ttime(self, text):
        """Parse for timetable time e.g. 12/34½"""
        return self._parse(text, "ttime")

    def parse_tmin(self, text):
        """Parse for timetable minute e.g. 4H"""
        return self._parse(text, "tmin")

    def parse_allowances(self, text):
        """Parse for timing point allowances e.g. <3H>"""
        return self._parse(text, "allowances")

    def parse_activity(self, text):
        """Parse for timing point activity e.g. N:1A01"""
        return self._parse(text, "activity")
