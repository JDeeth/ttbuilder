from enum import Flag, auto


class PowerType(Flag):
    """SimSig traction power categories

    Can be combined e.g. PowerType.DC_3RAIL | PowerType.AC_OVERHEAD"""

    NONE = 0
    AC_OVERHEAD = auto(), "O"
    DC_3RAIL = auto(), "3"
    DC_4RAIL = auto(), "4"
    DIESEL = auto(), "D"
    DC_OVERHEAD = auto(), "V"
    TRAMWAY = auto(), "T"
    SIM_1 = auto(), "X1"
    SIM_2 = auto(), "X2"
    SIM_3 = auto(), "X3"
    SIM_4 = auto(), "X4"

    def __new__(cls, flag, xml_value=""):
        obj = object.__new__(cls)
        obj._value_ = flag
        obj._xml_value = xml_value
        return obj

    @property
    def xml_value(self):
        """As used in SimSig .WTT"""
        code = getattr(self, "_xml_value", None)
        if code is None:
            # pylint: disable=protected-access
            code = "".join(pt._xml_value for pt in self)
            self._xml_value = code
        return code
