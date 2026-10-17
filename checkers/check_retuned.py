#!/usr/bin/env python3
"""Independent exact area checker: polynomial Taylor bounds and power sums.

Does not import the construction or its square-root certificate. For z>=0,
the degree-4 Taylor polynomial of (1+z)^(-1/2) is an upper bound and the
degree-5 polynomial is a lower bound, by Taylor's theorem and the sign of
the next derivative. All arithmetic here is rational or integer.
"""

from fractions import Fraction as F
from math import comb
import json


def add(a, b):
    out = [F(0)]*max(len(a), len(b))
    for i, value in enumerate(a):
        out[i] += value
    for i, value in enumerate(b):
        out[i] += value
    return out


def scale(a, c):
    return [x*c for x in a]


def mul(a, b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def power(a, n):
    out = [F(1)]
    for _ in range(n):
        out = mul(out, a)
    return out


def sum_polynomial(poly, n):
    sums = [n]
    for degree in range(1, len(poly)):
        numerator = (n+1)**(degree+1)-1
        numerator -= sum(comb(degree+1, j)*sums[j] for j in range(degree))
        assert numerator % (degree+1) == 0
        sums.append(numerator//(degree+1))
    return sum((coefficient*value for coefficient, value in zip(poly, sums)), F(0))


def bounds(e):
    # Positive cells [ (k-1)/5000, k/5000 ], k=1,...,5000.
    # Reflection supplies the 5000 negative cells; each cell has two families.
    e = F(e)
    mesh = F(1, 5000)
    q = [F(0), mesh]
    center = [F(-1, 10000), mesh]
    secant = [F(1, 2), -mesh**2/2, mesh**2/2]
    maximum = 1+e**2+F(9, 16)*e**4
    padding = (maximum*(e+e**2/2)+2*e**2+maximum*e**2/20000)/(10000*(1-e))
    cap = add([1+F(9, 16)*e**4+padding], scale(add(power(q, 2), power(q, 4)), e**2/2))
    z = scale(add(power(secant, 2), scale(power(center, 2), 2)), e**2)
    taylor = [F(1)]
    coefficient = F(1)
    output = {}
    for degree in range(1, 6):
        coefficient *= -F(2*degree-1, 2*degree)
        taylor = add(taylor, scale(power(z, degree), coefficient))
        if degree in (4, 5):
            result = sum_polynomial(mul(power(cap, 2), taylor), 5000)/10000
            output["upper" if degree == 4 else "lower"] = result
    return output


def main():
    new = bounds(F(13, 125))
    old = bounds(F(1, 10))
    assert new["upper"] < F(4999213, 10000000)
    assert old["lower"] > F(4999215, 10000000)
    assert new["upper"] < F("0.499921585997001774")
    # Give short outward decimal intervals too, without float conversion.
    result = {}
    for name, interval in [("candidate", new), ("baseline", old)]:
        out = {k: str(v) for k, v in interval.items()}
        s = 10**18
        out["decimal_lower_integer"] = str(interval["lower"].numerator*s//interval["lower"].denominator)
        u = interval["upper"]
        out["decimal_upper_integer"] = str(-(-u.numerator*s//u.denominator))
        out["decimal_scale"] = str(s)
        result[name] = out
    print(json.dumps(result, indent=2))
    print("PASS: independent rational Taylor/power-sum check proves strict improvement")


if __name__ == "__main__":
    main()
