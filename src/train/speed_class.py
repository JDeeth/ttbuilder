from enum import Flag


class SpeedClass(Flag):
    """SimSig speed restriction/easement categories

    Combine with |"""

    # EPS = Enhanced Permitted Speed - tilting trains
    EPS_E = 2**0
    EPS_D = 2**1
    HST = 2**2
    EMU = 2**3
    DMU = 2**4
    SPRINTER = 2**5
    CS_67 = 2**6
    MGR = 2**7
    TGV_373 = 2**8
    LOCO_H = 2**9
    METRO = 2**10
    WES_442 = 2**11
    TRIPCOCK = 2**12
    STEAM = 2**13
    SIM_1 = 2**24
    SIM_2 = 2**25
    SIM_3 = 2**26
    SIM_4 = 2**27

    @property
    def xml_value(self):
        """As used in SimSig .WTT"""
        return self.value
