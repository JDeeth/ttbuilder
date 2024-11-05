from functools import reduce
from lark import Lark, Transformer

from ttbuilder.common.activity import Activity
from ttbuilder.common.location import Location
from ttbuilder.common.timing_point import TimingPoint
from ttbuilder.common.train_id import TrainId
from ttbuilder.common.ttime import Allowance, TTime
from ttbuilder.simsig.local_timetable import LocalTimetable
from ttbuilder.train.power_type import PowerType
from ttbuilder.train.train_category import TrainCategory


class TransformTT(Transformer):
    """Transformer for timetable.lark"""

    # pylint: disable=missing-function-docstring,invalid-name

    def timing_point(self, args):
        location, ttime, allowances, activities = args
        allowances = [x for x in allowances or [] if x.time]
        ttime = TTime(ttime.seconds, ttime.stop_mode)

        return TimingPoint(
            location=location,
            depart=ttime,
            activities=list(activities or []),
            allowances=allowances,
        )

    def location(self, args):
        tiploc, platform = args
        return Location(tiploc=tiploc, platform=platform or "")

    def ttime(self, args):
        hour, stopmode, tmin = args
        return TTime(
            hour * 3600 + tmin.seconds,
            stopmode,
        )

    def HOUR(self, n):
        return int("".join(n))

    def stopmode(self, args):
        (mode,) = args
        return getattr(TTime.StopMode, mode.type, TTime.StopMode.PASSING)

    def tmin(self, args):
        minute, halfminute = args
        return TTime.from_hms(minutes=int(minute), seconds=30 if halfminute else 0)

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

    def activities(self, args):
        return list(args)

    def train_category(self, args):
        name, length, speed, *power_types = args
        power_types = [
            getattr(PowerType, pt.value.upper(), PowerType.NONE) for pt in power_types
        ]
        power_types = reduce(lambda x, y: x | y, power_types)
        return TrainCategory(
            description=name.value,
            length_m=int(length.value),
            max_speed_mph=int(speed.value),
            power_type=power_types,
        )

    def timetable(self, args):
        train_id, train_desc, *timing_points = args
        origin_dep, origin, dest, tc_name = train_desc.children
        return LocalTimetable(
            train_id=train_id,
            train_type=tc_name,
            origin=origin,
            origin_dep=origin_dep,
            destination=dest,
            timing_points=timing_points,
        )


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

    def parse_train_category(self, text):
        """Parse for train category description"""
        return self._parse(text, "train_category")

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

    def parse_timetable(self, text):
        """Parse train timetable"""
        return self._parse(text, "timetable")
