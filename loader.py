#!/usr/bin/env python3

# Reads data.txt into {region: [(name, x, y, lat, lon), ...]}.
#   [region]        starts a new Run8 coordinate frame
#   # ...           comment, anywhere on a line
#   name X,Y lat,lon   name may contain spaces; the last two fields are the pairs

def split_pair(pair):
    toks = pair.split(",")
    return float(toks[0]), float(toks[1])

def load_file(path="data.txt"):
    regions = {}
    region = "default"
    with open(path, "r") as df:
        for num, line in enumerate(df, 1):
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                region = line[1:-1].strip()
                continue
            try:
                name, xy, ll = line.rsplit(None, 2)
                x, y = split_pair(xy)
                lat, lon = split_pair(ll)
            except ValueError:
                print("data.txt line %d: can't read '%s' (want: name X,Y lat,lon)" % (num, line))
                continue
            regions.setdefault(region, []).append((name, x, y, lat, lon))
    return regions
