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

    def __new__(cls, flag, xml_code=""):
        obj = object.__new__(cls)
        obj._value_ = flag
        obj._xml_code = xml_code
        return obj

    def xml_value(self):
        """As used in SimSig .WTT"""
        # pylint: disable=W0212
        return "".join(pt._xml_code for pt in PowerType if pt & self)
