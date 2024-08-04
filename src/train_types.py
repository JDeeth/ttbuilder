from dataclasses import dataclass
from lxml import etree

from cajontime import CajonTime

"""
# Train types

- Description
- Length (m)
- Accel/Brake Rate
  - Very low (slow freight)
  - Low (standard freight)
  - Medium (intercity)
  - High (commuter)
  - Very high (light loco / metro)
- Max speed (mph)
- Weight
  - Normal
  - Light
  - Heavy
- Defensive driving
- Power types (multiselect)
  - Overhead AC
  - 3rd rail
  - 4th rail
  - Diesel
  - Overhead DC
  - Tramway
  - Sim 1-4
- Speed classes: (multiselect)
  - EPS-E, EPS-D, HST, EMU, DMU, SP, CS (CL67), MGR, TGV (CL373), Loco-H, Metro, WES (CL442), Tripcock, Steam, Sim 1-4
- Use freight linespeeds
- Can use freight lines
- Dwell times
  - Red signal move off
  - Crew change
  - Station forward
  - Station reverse
  - Terminate forward
  - Terminate reverse
  - Join
  - Divide

from wiki:
<TrainCategory> 
attribute ID 	an empty or missing value is replaced by a random 8 digit hexadecimal number
<Description> 	default %%''%% 	
<AccelBrakeIndex> 	default 0 	
<IsFreight> 	default False 	use goods speeds
<CanUseGoodsLines> 	default False 	
<MaxSpeed> 	default 0 	
<TrainLength> 	default 0 	
<SpeedClass> 	default 0 	[SC]
<PowerToWeightCategory> 	default 0 	{ Normal, Light, Heavy }
<Electrification> 	default %%''%% 	[3]
<CautionSpeedSet> 	default %%''%% 	contains the ID attribute of a <CautionSpeedSet>
<DwellTimes> 	list 	contains <DwellTime>
"""


@dataclass
class DwellTimes:
    red_signal_move_off: CajonTime = CajonTime(0)
    station_forward: CajonTime = CajonTime(0)
    station_reverse: CajonTime = CajonTime(0)
    terminate_forward: CajonTime = CajonTime(0)
    terminate_reverse: CajonTime = CajonTime(0)
    join: CajonTime = CajonTime(0)
    divide: CajonTime = CajonTime(0)
    crew_change: CajonTime = CajonTime(0)

    def xml(self):
        result = etree.Element("DwellTimes")
        etree.SubElement(result, "RedSignalMoveOff").text = str(
            self.red_signal_move_off.seconds
        )
        etree.SubElement(result, "StationForward").text = str(
            self.station_forward.seconds
        )
        etree.SubElement(result, "StationReverse").text = str(
            self.station_reverse.seconds
        )
        etree.SubElement(result, "TerminateForward").text = str(
            self.terminate_forward.seconds
        )
        etree.SubElement(result, "TerminateReverse").text = str(
            self.terminate_reverse.seconds
        )
        etree.SubElement(result, "Join").text = str(self.join.seconds)
        etree.SubElement(result, "Divide").text = str(self.divide.seconds)
        etree.SubElement(result, "CrewChange").text = str(self.crew_change.seconds)
        return result
