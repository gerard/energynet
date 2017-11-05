# Mathy utility code
import re
import time
import math

def sin_variate(min_val, max_val, period_ms):
    t = time.time() * 1000
    t %= period_ms              # t in [0, period_ms]
    t -= period_ms / 2          # t in [-period_ms/2, period_ms/2]
    t /= period_ms              # t in [-1/2, 1/2]
    t *= math.pi * 2            # t in [-pi, pi]

    v = math.sin(t)             # v in [-1, 1] (sin)
    v = (v + 1) / 2             # v in [0, 1] (sin)
    ret = min_val + (max_val - min_val) * v

    return min(max_val, max(min_val, ret))

def lin_variate(min_val, max_val, period_ms):
    t = time.time() * 1000
    t %= period_ms
    delta = max_val - min_val
    delta /= (t / period_ms)
    return min_val + delta

def split_line(fro, to, divs=7):
    ret = []
    shift = sin_variate(-1, 1, 4000)
    delta = (to[0] - fro[0], to[1] - fro[1])
    delta = (delta[0] / float(divs), delta[1] / float(divs))
    for i in range(divs):
        if i % 2 == 0:
            continue

        k = i + shift
        ret.append((
            (fro[0] + delta[0] * k, fro[1] + delta[1] * k),
            (fro[0] + delta[0] * (k + 1), fro[1] + delta[1] * (k + 1)),
        ))

    return ret

# Sort a list of 2D points in clowise order relative to an origin point.  Pass
# ancilliary data by (ab)using extra fields in the point tuple: (x, y, mydata).
#       N P4
#       |/          # In this case, the order should be P4, P2, P1, P3.  The
#    P3-O---P2      # calculation is done based on the cross product each of
#        \          # the vectors against (O, N)
#         \
#          P1
def cwise_sort(orig, plist):
    def normalize(v):
        norm = math.sqrt(v[0]**2 + v[1]**2)
        return (v[0] / norm, v[1] / norm)

    def xproduct(v, w):
        return v[0] * w[1] - v[1] * w[0]

    def cwise_key(p):
        # We reverse the Y coordinate because display coordinates grow when
        # going *down*, while cartesian coordinates grow when going *up*
        v = ((p[0] - orig[0]), -(p[1] - orig[1]))
        v = normalize(v)

        # Each if clause refers to each of the quadrants of the plane, the
        # crossproduct is calculated against the "smaller" angle of that
        # quadrant.  Since the v is normalized, we know the range of the cross
        # product is [0, 1] (and the calculations on the full plane can be
        # mapped to [0, 4])
        if v[0] >= 0:
            if v[1] >= 0:
                r = xproduct(v, (0, 1))
            else:
                r = 1 + xproduct(v, (1, 0))
        else:
            if v[1] < 0:
                r = 2 + xproduct(v, (0, -1))
            else:
                r = 3 + xproduct(v, (-1, 0))
        return r

    return sorted(plist, key=cwise_key)

def camel2underscore(s):
    s = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s.lower())
