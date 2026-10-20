XY2LatLon - Run8 X,Y to real-world lat,lon
==============================================

Warranty: here it is. Good luck!

What it does
  Run8 shows your position as X,Y. Measure a handful of places where you know
  both the X,Y (from the game) and the lat,lon (from any map), put them in
  data.txt, and find.py fits a straight-line (affine) transform between the two.
  Then you can convert any X,Y in that region.

Usage (needs only Python 3)
  python3 find.py                 how good each region's fit is
  python3 find.py socal           same, then type X,Y pairs to convert
  python3 find.py socal 176,-88   convert one point

data.txt
  name   X,Y   lat,lon          names may contain spaces
  [region]                      starts a new region
  # comment                     anywhere on a line

  Each Run8 region has its own coordinate grid. The SoCal fit would put
  Fitzgerald in central California, so every region gets its own [section]
  and its own points. A region needs at least 3 points to fit; aim for 6+,
  spread out across the whole route, not bunched in one corner.

Accuracy
  With the included SoCal points: about 0.5 km typical, under 3 km worst.
  That is the limit of the input, not the math: the lat,lons have 2 decimals
  and the X,Ys are whole numbers (one unit is about 1 km), so each point is
  already rounded by about half a kilometre. 

  Good enough to tell you roughly where you are. Not good enough to tell which
  track in a yard you're on.

Checking your points
  The report refits without each point in turn and prints how far off that
  point lands. One point much worse than the rest is almost always a typo or
  a misread X,Y. Ash Hill is currently the suspect one.

Files
  find.py      the fit and converter
  loader.py    reads data.txt
  data.txt     the reference points

Usage example:

$ ./find.py 
[socal] 20 points
  Saco              0.50 km
  Kern Jct          0.43 km
  Palmdale          1.29 km
  Mojave            0.07 km
  Hinkley           0.59 km
  Hutt              0.50 km
  Lenwood           0.71 km
  Daggett           0.52 km
  Minneola          0.53 km
  Ash Hill          2.68 km
  Needles           1.92 km
  Hodge             0.47 km
  Cajon             1.12 km
  W Colton X        1.30 km
  LA J Yard         0.94 km
  Dayton Pkwy OP    0.12 km
  Los Nietos X      0.28 km
  Fullerton Jct     0.52 km
  Ontario           0.38 km
  Streeter          0.62 km
  median 0.53 km, worst 2.68 km
[southeast] 9 points
  Stanton Energy    1.46 km
  Deland Amtrak     0.21 km
  Bostwick          0.11 km
  Fitzgerald        0.68 km
  Campground        0.83 km
  MP 788.3          0.45 km
  Sanderson         1.73 km
  Jesup             0.60 km
  Salkehatchie      1.89 km
  median 0.68 km, worst 1.89 km

$ ./find.py socal 89,4
35.04004, -118.17072
