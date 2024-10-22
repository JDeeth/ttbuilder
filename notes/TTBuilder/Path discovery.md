1. Load a sim with a blank timetable
2. For each route in the sim, create a train which only includes intermediate timing points where it's required for a valid timetable.
	- The routes need not overlap
	- Branches can be mapped with a train running from the terminus/entrypoint to the junction and back
3. For each route, create another train that includes every possible timing point along the way
	- This can be skipped for routes where all the intermediate points are mandatory
	- There are sometimes no valid paths between adjacent junctions. TBD how to deal with this
4. Add trains for station manoeuvres such as running round a train, shunting between platforms
5. From the above, extract:
	- the set of valid links between timing points
	- the set of mandatory timing points
	- codified station manoeuvres

Currently there is a .SSG parser that shows the sequence of each train.

Perhaps:

| `1xxx` | minimal stops |
| ------ | ------------- |
| `2xxx` | all stops     |
| `xAxx` | main routes   |
| `xBxx` | branch routes |
| `xSxx` | shunt routes  |
## Worked example - Wembley Suburban

![[Wembley Suburban diagram.png]]
### Routes
- Camden Jn - Watford Junction
- Bakerloo line - Kensal Green
- Kensal Green Jn - Willesden Junction
- Willesden TMD - Willesden Junction
- Stonebridge depot - Stonebridge Park station
- Croxley Green - Watford High St
- Cardiff Rd CEGB - Watford High St
- Watford Junction - Watford Sidings
- Watford Junction - WCML
### Station manoeuvres
- Watford Junction platform change reversing at signal 309
- Harrow and Wealdstone reversing at signals 305 and 307
- Willesden Junction reverse at signals 301 and 303
#### Camden Jn - Watford Jn minimal points
Let's make a train that runs from Camden Green Jn to Watford Junction and back, calling only at mandatory timing points.
- Create a train, headcode 1A01, entry point Camden Jn
- Add Watford Jn (DC) as a location
- Press "Validate". The "Next Key Locations" messagebox opens to advise there are no paths from Camden Jn to Watford Junction, and shows some of the locations which are:  
    ![[Camden Jn key locations.png]]

- Pick the furthest possible option - in this case there's only one option, Kilburn High Road - and add that to the location list
- Repeat the process along the route. At Willesden Junction you will be required to pick a platform. Platform 2 is a bay so pick platform 3.
- At Watford Junction you will be required to pick a platform again:  
  ![[Camden - Watford with autoinsert.png]]
- At this point we can remove Platform 3 from Willesden Junction and click "Clear Autoinsert" to remove the path and line codes. The resulting timetable is still valid - if you click "Validate" Platform 3 comes back along with the path and line codes, because they are unambiguous here. We can create a timetable with just these timing points and only a platform code at Watford Junction, and the unambiguous missing details will be automatically inserted when SimSig uses the timetable.  
  ![[Camden - Watford without autoinsert.png]]
- We can run this same train back to Camden Jn to complete the loop. If the train ran from a sim boundary to a sim boundary, we'd need a second train for the return journey to include the second entrypoint.
- SimSig will also insert mandatory timing points as passing places in some circumstances - see Kilburn High Road in title case here.  
  ![[Camden - Watford - Camden with autoinsert.png]]  
  For consistency, open the location and press OK to make it manually-entered, which makes the name upper-case. The click "Clear autoinsert" - again, we want only the points the timetable **must** provide, not what SimSig can infer for itself.
### Camden Jn - Watford Junction all points
- Create another train, 2A01, entering at Camden Jn
- Insert every timing point you see on the route between there and Watford Junction and back
- When getting near the sim boundary at South Hampstead, add a location that's unreachable from there to force the Next Key Location window to show
- Press Validate and from the Next Key Location window, you may see relevant offscreen timing points. Here there's only Camden Jn:  
  ![[Kilburn next key locations.png]]
- A "gotcha" here is Queens Park Jn - where the Bakerloo Line joins the Watford Suburban line. It's not labelled on the panel but it's a valid timing point between Kensal Green and Queens Park.
- Change the final locations to valid ones and ensure the timetable validates
- Remove as much detail as possible, Validate, and Clear Autoinsert once more
- That's it - 2A01 describes the full physical route, and 1A01 describes the mandatory points along it!
### Bakerloo Line
This was a bit more complicated - on this sim, the trains enter at "Bakerloo Line" having already departed Queens Park, so the next point is Queens Park Jn. From there we already know the path to Stonebridge and Harrow but SimSig won't accept a timetable as valid without at least one key location. So we need to extend the trip to Willesden Jn. For the return journey, there's no "off-sim" timing point beyond Queens Park. Southbound Bakerloo trains just go to Queens Park platform 2 via path LU:
![[Queens Park - Willesden Jn return.png]]
The lack of an off-sim timing point (for Kilburn Park, say) means some additional work (what exactly that work is is TBC) to show that southbound Bakerloo trains must use Queens Park platform 2 pathed via LU - it would be clearer if we could add Kilburn Park onto this timetable for that purpose.
### Kensal Green Jn
We need a path from the entrypoint to somewhere we've already mapped - which is right there, Willesden Jn. So 2B02 enters at Kensal Green Jn and travels to Willesden Junction then right back to Kensal Green Jn. Much simpler.
### Willesden Junction shunt moves
0S01 enters at Willesden TMD and reverses on both sides of the station, then runs back to the TMD. The platform numbers are not telling the complete story here.
![[Willesden shunts.png]]
### Stonebridge depot
There are two entrypoints so we'd need two trains: depot > signal 34 > Stonebridge Park and back, and depot > signal 34 only. Trains can bypass signal 34 but we can omit that detail.
![[Stonebridge Depot shunts.png]]
### Harrow shunt moves
This can run from the station to each reversing point in turn and back:

![[Harrow shunts.png]]
### Croxley Green branch
This can be mapped with three trains:
- 2B03 Cardiff Rd CEGB entrypoint > Watford High St > Cardiff Rd CEGB
- 2B04 Watford High Street > Croxley Green and back, all stations
- 1B04 Watford High Street > Croxley Green and back, no intermediate stations
These all validate OK.
### Watford Junction area
- 2S05 Watford Jn P6 and Watford Jn DC to/from Watford South (Rev.)
- 2S06 Watford Jn Sdgs to/from Watford Jn P6
- 2S07 Watford High Street to/from Watford Jn P6
- 2S08 Watford Jn Dn Fast > P6 > Watford dep south
- 2S09 Watford Jn Dn Slow > P6 > Watford dep north
### Extracting the paths
Save the timetable as e.g. `WFJ pathfinding.WTT` (WFJ being the [[CRS code]] for Watford Junction)
Then save the game (the [[.SSG]] file includes more information about the sim e.g. all the entry and timing points)
Run `ttbuilder` and give the path to the save game file, and the results will be parsed out:
![[Wembley SSG parsed.png]]
This shows the locations the pathfinding has not found. `EWJP6` is probably Watford Jn Platform 6 and isn't in the list of entrypoints - perhaps a legacy of an earlier sim version. Likewise the locations not in timetables - some relate to reversing at the ground frame crossover at Wembley Central, the others may be legacy or could be mapped in as-needed.

`EPHT` and `WATRLLT` are Elephant & Castle and Waterloo Underground stations and are possibly the "missing" off-sim timing points for Bakerloo trains. Unfortunately with some experimentation manually inserting them into .WTT files, they are not valid timing points for inclusion after `QPRK`.
