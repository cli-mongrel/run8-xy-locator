#!/usr/bin/env python3

# Run8 X,Y -> lat,lon by a least-squares affine fit over hand-measured points.
#   find.py                list the regions and how good each fit is
#   find.py socal          fit report, then type X,Y pairs to convert
#   find.py socal 176,-88  convert one point and exit

import math
import sys

# import numpy as np

import loader

MIN_POINTS = 3

# numpy versions, replaced by the plain-Python ones below:
# def fit(points):
#     # lat = a*x + b*y + c and lon = d*x + e*y + f, solved together
#     A = np.array([[p[1], p[2], 1.0] for p in points])
#     L = np.array([[p[3], p[4]] for p in points])
#     return np.linalg.lstsq(A, L, rcond=None)[0]
#
# def transform(coeffs, x, y):
#     lat, lon = np.array([x, y, 1.0]) @ coeffs
#     return lat, lon

def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
          - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
          + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

def solve3(m, v):
    # Cramer's rule: swap v into each column in turn
    d = det3(m)
    if abs(d) < 1e-12:
        raise ValueError("points are all on one line - can't fit")
    out = []
    for col in range(3):
        mc = [row[:] for row in m]
        for r in range(3):
            mc[r][col] = v[r]
        out.append(det3(mc) / d)
    return out

def fit(points):
    # lat = a*x + b*y + c and lon = d*x + e*y + f, by least squares.
    # Normal equations, with X,Y centred on their means so the sums stay
    # similar in size (the matrix is the same for lat and lon).
    n = len(points)
    mx = sum(p[1] for p in points) / n
    my = sum(p[2] for p in points) / n
    xs = [p[1] - mx for p in points]
    ys = [p[2] - my for p in points]
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    syy = sum(y * y for y in ys)
    sx, sy = sum(xs), sum(ys)
    m = [[sxx, sxy, sx],
         [sxy, syy, sy],
         [sx,  sy,  n]]
    coeffs = [mx, my]
    for k in (3, 4):            # lat, then lon
        t = [p[k] for p in points]
        v = [sum(x * a for x, a in zip(xs, t)),
             sum(y * a for y, a in zip(ys, t)),
             sum(t)]
        coeffs.append(solve3(m, v))
    return coeffs               # [mean x, mean y, (a,b,c) lat, (d,e,f) lon]

def transform(coeffs, x, y):
    mx, my, cl, cn = coeffs
    x, y = x - mx, y - my
    lat = cl[0] * x + cl[1] * y + cl[2]
    lon = cn[0] * x + cn[1] * y + cn[2]
    return lat, lon

def km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    c = math.sin(p1) * math.sin(p2) + math.cos(p1) * math.cos(p2) * math.cos(dl)
    return 6371.0 * math.acos(min(1.0, c))

def report(name, points):
    # Leave-one-out: refit without each point, then see how far off it lands.
    # Needs 4+ points to mean anything; a point far worse than the rest is a typo.
    print("[%s] %d points" % (name, len(points)))
    if len(points) <= MIN_POINTS:
        return
    errs = []
    for i, p in enumerate(points):
        c = fit(points[:i] + points[i+1:])
        e = km(p[3], p[4], *transform(c, p[1], p[2]))
        errs.append(e)
        print("  %-16s %5.2f km" % (p[0], e))
    errs.sort()
    print("  median %.2f km, worst %.2f km" % (errs[len(errs) // 2], errs[-1]))

def convert(coeffs, text):
    x, y = (float(t) for t in text.replace(" ", "").split(","))
    lat, lon = transform(coeffs, x, y)
    print("%.5f, %.5f" % (lat, lon))

regions = loader.load_file()

if len(sys.argv) < 2:
    for name, points in regions.items():
        if len(points) < MIN_POINTS:
            print("[%s] %d point(s) - need at least %d" % (name, len(points), MIN_POINTS))
        else:
            report(name, points)
    sys.exit(0)

name = sys.argv[1]
if name not in regions:
    sys.exit("no region [%s] in data.txt (have: %s)" % (name, ", ".join(regions)))
points = regions[name]
if len(points) < MIN_POINTS:
    sys.exit("[%s] has %d point(s) - need at least %d" % (name, len(points), MIN_POINTS))
coeffs = fit(points)

if len(sys.argv) > 2:
    convert(coeffs, "".join(sys.argv[2:]))
    sys.exit(0)

report(name, points)
while True:
    try:
        text = input("enter X,Y: ").strip()
    except EOFError:
        break
    if not text:
        break
    try:
        convert(coeffs, text)
    except ValueError:
        print("want X,Y like 176,-88")
