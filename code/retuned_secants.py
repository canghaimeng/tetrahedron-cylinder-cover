#!/usr/bin/env python3
"""Exact retuning of van de Kamp's compatible-secant construction.

Adapted mathematical definitions from SECANT-THEOREM.md at upstream commit
db6e1d89a0637b013a86464bd766c0a5120e454e. This implementation reconstructs those definitions directly.
The coverage proof, valid for 0 < epsilon < 1, is in ../main.tex.
No sampled containment test is used.
"""

import argparse
from fractions import Fraction as F
import json
from math import isqrt
from pathlib import Path


def parameters(epsilon, n):
    e = F(epsilon)
    if not 0 < e < 1 or not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("Require 0 < epsilon < 1 and a positive integer n")
    a = F(1, n)
    maximum = 1 + e**2 + F(9, 16)*e**4
    k0 = maximum*(e + e**2/2) + 2*e**2
    delta = (k0*a + maximum*e**2*a**2/2)/(1-e)
    return e, a, delta


def cell(e, a, delta, index):
    left = -1 + 2*index*a
    right = left + 2*a
    center = (left+right)/2
    secant = (1+left*right)/2
    q = max(abs(left), abs(right))
    cap = 1 + e**2*(q**2+q**4)/2 + F(9, 16)*e**4 + delta
    norm_squared = 1 + e**2*(secant**2+2*center**2)
    # Normalized area of the two cylinders in this cell is numerator/sqrt(Q).
    numerator = a*cap**2/2
    return left, right, center, secant, cap, numerator, norm_squared


def certificate(epsilon, n, digits=25):
    e, a, delta = parameters(epsilon, n)
    scale = 10**digits
    lower_integer = 0
    for index in range(n):
        *_, numerator, norm_squared = cell(e, a, delta, index)
        square = numerator**2/norm_squared
        k = isqrt(square.numerator*scale**2 // square.denominator)
        assert k*k*square.denominator <= square.numerator*scale**2
        assert (k+1)**2*square.denominator > square.numerator*scale**2
        lower_integer += k
    return {
        "epsilon": str(e), "n": n, "cylinder_count": 2*n,
        "scale": str(scale), "lower_integer": str(lower_integer),
        "upper_integer": str(lower_integer+n),
        "lower": str(F(lower_integer, scale)),
        "upper": str(F(lower_integer+n, scale)),
        "upper_is_strict": True,
        "padding": str(delta),
    }


def dot(u, v):
    return u[0]*v[0]+u[1]*v[1]+2*u[2]*v[2]


def cylinder(epsilon, n, index):
    if not 0 <= index < 2*n:
        raise ValueError("Cylinder index outside range")
    e, a, delta = parameters(epsilon, n)
    family, j = divmod(index, n)
    left, right, center, secant, cap, numerator, norm_squared = cell(e, a, delta, j)
    t = cap/2
    if family == 0:
        axis = (F(1), e*secant, e*center)
        vertices = [(F(0), F(0), F(0)), (F(0), left*t, t), (F(0), right*t, t)]
    else:
        axis = (-e*secant, F(1), e*center)
        vertices = [(F(0), F(0), F(1)), (left*t, F(0), 1-t), (right*t, F(0), 1-t)]
    projected = []
    for vertex in vertices:
        ratio = dot(vertex, axis)/norm_squared
        projected.append(tuple(x-ratio*y for x, y in zip(vertex, axis)))
    return {
        "epsilon": str(e), "n": n, "index": index,
        "coordinate_convention": "(x,y,z/sqrt(2)); metric diag(1,1,2)",
        "axis": axis, "intercept_vertices": vertices,
        "perpendicular_vertices": projected,
        "area_over_Amin": {"numerator": numerator/2, "sqrt_denominator": norm_squared},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--index", type=int)
    args = parser.parse_args()
    if args.index is not None:
        result = cylinder(F(13, 125), 10000, args.index)
    else:
        new = certificate(F(13, 125), 10000)
        old = certificate(F(1, 10), 10000)
        assert F(new["upper"]) < F(4999213, 10000000)
        assert F(old["lower"]) > F(4999215, 10000000)
        assert F(new["upper"]) < F("0.499921585997001774")
        result = {
            "candidate": new, "baseline": old,
            "threshold": "0.499921585997001774",
            "comparison": "R_new < 4999213/10000000 < 4999215/10000000 < R_old",
            "status": "Exact arithmetic certificate; see ../result.json for proof status",
        }
    output = json.dumps(result, default=str, indent=2)+"\n"
    if args.output:
        args.output.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
