# Timetable Builder

This will be a SimSig timetable builder, intended to allow chained timetables
to be built easily.

## Example - 1M45

1M45 was a night train, which the Railtrack Sept 1995 WTT shows ran from
Peterborough to Carlisle via Derby, Lichfield Trent Valley and Crewe.

![Trent Jn 23/55H to Derby 00:13](img/1M45%20-%20Derby.png "1M45 timetable before Derby")
![Derby 00:40 to Lichfield TV Jn 01/06H](img/1M45%20Derby-LTV.png "1M45 timetable Derby-LTV")
![Lichfield TV Jn 01/06H to Crewe Basford Hall Jn 01/46](img/1M45%20LTV-Crewe.png "1M45 timetable LTV-Crewe")

The aim is to generate compatible timetable files for specified SimSig sims,
including neighbouring sims for large multiplayer games. 1M45 can run through
the Derby, Aston and Stafford sims:

![Hand-written 1M45 timetables in each sim](img/1M45%20SimSig%20timetables.png "Popup timetables for 1M45 in each sim")

Hand-written timetables for 1M45 are included in [tests/sample/1M45](tests/sample/1M45)

The user input would be a description of the train and the same timing
information as in the actual WTT. Something like this, using real-world TIPLOCs:

```
Parcels:
220m, 90mph, Diesel
Dwell times 0:05, 3:00, 1:00, 1:00, 1:00, 1:00, 5:00, 2:00

1M45
22:30 Peterborough-Carlisle (Parcels)
TRENTJ  23/55H
SHEETSJ 23/56
SPDN    00/01
DRBY    00:13 [4] <4> 6 Runround
DRBY    00:40
STSNJN  00/47H [0H]
NSJDRBY 00/48H
BURTNOT 00/53
WICHNRJ 00/58H
LCHTTVJ 01/06H
LCHTTVL 01/09 FL
ARMITAG 01/14H
COLWICH 01/19H
MILFDY  01/21H SL
STAFFRD 01/25 5
NTNB    01/29H
MADELEY 01/37H
CREWBHJ 01/46 [3]
```

The user/admin would also provide a mapping between the real WTT timing point
sequence and the required SimSig locations, e.g. estimating times for North
Staffordshire Junction and Alrewas L.C.

The `Runround` statement would generate a timetable for the train engine to
carry out a typical run-round for the location, e.g.  
`Derby > Derby S.N.J (462) > Derby > Derby (439) > Derby J:1M45`

The user should be able to specify seed points, and trains operating at the
seed point boundary should break at that point. Specifying the seed point
location (e.g. signal Derby 404 for 1M45 at 00:00) would be nice.

## Timetable planning

- Provide typical stopping pattern and timings
- Generate timetable for train by providing just the train ID, departure time
- Generate variations by adding a time variation for a TIPLOC
- Show unbalanced workings (train does not come from or go onwards to anywhere)
- Provide method to draft train working diagrams
- Show full timetable in the traditional WTT format

## TRUST (eventually)

- Terminal-style TUI interface to show entire timetable
- SimSig Gateway integration for timing performance
- Make new/altered workings in TUI and generate .wtt files for host to import?

## Development notes

- Configure your computer to [open .WTT files as .zip](https://superuser.com/a/1858317/677515)
- To activate virtual environment in Powershell: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`