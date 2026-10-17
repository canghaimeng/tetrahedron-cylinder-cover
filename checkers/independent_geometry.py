#!/usr/bin/env python3
"""Independent exact checks of the retuned area and overlap identity.

Does not import retuned_secants.py or check_retuned.py.
Uses only pinned SECANT-THEOREM.md formulas.
"""
from fractions import Fraction as F
from math import isqrt, comb
from collections import defaultdict

N = 10000
SCALE = 10**25
THRESH = F("0.499921585997001774")
R13 = F(4999213, 10000000)
R15 = F(4999215, 10000000)


class Poly(dict):
    """Sparse polynomial in e,p,q. Keys are (de, dp, dq)."""

    def __init__(self, data=None):
        super().__init__()
        if data:
            for k, v in data.items():
                if v:
                    self[k] = F(v)

    def __add__(self, other):
        if not isinstance(other, Poly):
            other = Poly({(0, 0, 0): other})
        out = Poly(self)
        for k, v in other.items():
            out[k] = out.get(k, 0) + v
            if out[k] == 0:
                del out[k]
        return out

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, Poly) else Poly({(0, 0, 0): -other}))

    def __mul__(self, other):
        if not isinstance(other, Poly):
            other = Poly({(0, 0, 0): other})
        out = defaultdict(lambda: F(0))
        for (a, b, c), u in self.items():
            for (d, e, f), v in other.items():
                out[(a + d, b + e, c + f)] += u * v
        return Poly(out)

    def __rmul__(self, other):
        return self * other

    def __pow__(self, n):
        out = Poly({(0, 0, 0): 1})
        for _ in range(n):
            out = out * self
        return out


E = Poly({(1, 0, 0): 1})
P = Poly({(0, 1, 0): 1})
Q = Poly({(0, 0, 1): 1})
ONE = Poly({(0, 0, 0): 1})


def G(var):
    return (ONE + var * var) * F(1, 2)


def D(var):
    return (ONE - var * var) * F(1, 2)


def h(var):
    return (var * var) * G(var)


def C(var):
    return ONE + (E * E) * h(var) + F(9, 16) * (E ** 4)


def identity_difference():
    N0 = ONE + (E * E) * G(P) * G(Q)
    Am = ONE - E * P * Q + (E * E) * G(P) * D(Q)
    Bp = ONE + E * P * Q + (E * E) * G(Q) * D(P)
    lhs = Am * C(Q) + Bp * C(P) - F(2) * N0
    S = ONE + P * P + Q * Q
    sq = (P * P - Q * Q + E * P * Q * S * F(1, 2)) ** 2
    t1 = (E * E * F(1, 2)) * sq
    t2 = (E ** 4) * (
        G(P) * G(Q) * (P * P * D(P) + Q * Q * D(Q))
        + (Poly({(0, 0, 0): 9}) - (P * P) * (Q * Q) * (S * S)) * F(1, 8)
    )
    t3 = F(9, 16) * (E ** 6) * (G(P) * D(Q) + G(Q) * D(P))
    rhs = t1 + t2 + t3
    return lhs - rhs


def area_bounds(e):
    e = F(e)
    a = F(1, N)
    mstar = 1 + e * e + F(9, 16) * e**4
    k0 = mstar * (e + e * e / 2) + 2 * e * e
    delta = (k0 * a + mstar * e * e * a * a / 2) / (1 - e)
    lower = 0
    for i in range(N):
        left = -1 + 2 * i * a
        right = left + 2 * a
        center = (left + right) / 2
        secant = (1 + left * right) / 2
        q = max(abs(left), abs(right))
        cap = 1 + e * e * (q * q + q**4) / 2 + F(9, 16) * e**4 + delta
        z = 1 + e * e * (secant * secant + 2 * center * center)
        num = a * cap * cap / 2
        square = num * num / z
        u, v = square.numerator, square.denominator
        k = isqrt(u * SCALE * SCALE // v)
        if k * k * v > u * SCALE * SCALE:
            raise AssertionError("isqrt overestimate")
        if (k + 1) * (k + 1) * v <= u * SCALE * SCALE:
            raise AssertionError("isqrt interval not strict upper")
        lower += k
    return {
        "delta": delta,
        "mstar": mstar,
        "lower_int": lower,
        "upper_int": lower + N,
        "lower": F(lower, SCALE),
        "upper": F(lower + N, SCALE),
    }


def taylor_half_sum(e):
    e = F(e)
    mesh = F(1, 5000)
    mstar = 1 + e * e + F(9, 16) * e**4
    padding = (mstar * (e + e * e / 2) + 2 * e * e + mstar * e * e / 20000) / (
        10000 * (1 - e)
    )

    def mul(a, b):
        out = [F(0)] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i + j] += x * y
        return out

    def add(a, b):
        out = [F(0)] * max(len(a), len(b))
        for i, x in enumerate(a):
            out[i] += x
        for i, y in enumerate(b):
            out[i] += y
        return out

    def scale(a, c):
        return [x * c for x in a]

    def power(a, n):
        out = [F(1)]
        for _ in range(n):
            out = mul(out, a)
        return out

    def faulhaber_sum(poly_coeffs, n):
        sums = [n]
        for degree in range(1, len(poly_coeffs)):
            numerator = (n + 1) ** (degree + 1) - 1
            numerator -= sum(comb(degree + 1, j) * sums[j] for j in range(degree))
            assert numerator % (degree + 1) == 0
            sums.append(numerator // (degree + 1))
        return sum(c * s for c, s in zip(poly_coeffs, sums))

    q = [F(0), mesh]
    center = [F(-1, 10000), mesh]
    secant = [F(1, 2), -mesh**2 / 2, mesh**2 / 2]
    cap = add(
        [1 + F(9, 16) * e**4 + padding],
        scale(add(power(q, 2), power(q, 4)), e * e / 2),
    )
    z = scale(add(power(secant, 2), scale(power(center, 2), 2)), e * e)
    taylor = [F(1)]
    coefficient = F(1)
    out = {}
    for degree in range(1, 6):
        coefficient *= -F(2 * degree - 1, 2 * degree)
        taylor = add(taylor, scale(power(z, degree), coefficient))
        if degree in (4, 5):
            result = faulhaber_sum(mul(power(cap, 2), taylor), 5000) / 10000
            out["upper" if degree == 4 else "lower"] = result
    out["padding"] = padding
    return out


def first_crossing_endpoints():
    e = F(13, 125)
    Nloc = 10000
    a = F(1, Nloc)
    verts = [
        ("(+1,0,0)", F(1), F(0), F(0)),
        ("(-1,0,0)", F(-1), F(0), F(0)),
        ("(0,+1,H)", F(0), F(1), F(1)),
        ("(0,-1,H)", F(0), F(-1), F(1)),
    ]
    checks = []
    for name, x, y, s in verts:
        assert abs(x) <= 1 - s
        assert abs(y) <= s
        F0 = s * F(-1) + e * x * F(0)
        FN = s * F(1) + e * x * F(0)
        assert F0 == -s
        assert FN == s
        assert F0 <= y <= FN
        k = None
        for j in range(1, Nloc + 1):
            q = -1 + 2 * j * a
            Dq = (1 - q * q) / 2
            Fk = s * q + e * x * Dq
            if Fk >= y:
                k = j
                break
        assert k is not None
        i = k - 1
        left = -1 + 2 * i * a
        right = left + 2 * a
        center = (left + right) / 2
        Ai = (1 + left * right) / 2
        t0 = s - e * x * center
        y0 = y - e * x * Ai
        assert t0 >= 0
        assert left * t0 <= y0 <= right * t0
        E0 = (1 - s) * F(-1)
        EN = (1 - s) * F(1)
        assert E0 <= x <= EN
        k2 = None
        for j in range(1, Nloc + 1):
            q = -1 + 2 * j * a
            Dq = (1 - q * q) / 2
            Ek = (1 - s) * q - e * y * Dq
            if Ek >= x:
                k2 = j
                break
        assert k2 is not None
        jcell = k2 - 1
        left2 = -1 + 2 * jcell * a
        right2 = left2 + 2 * a
        c2 = (left2 + right2) / 2
        A2 = (1 + left2 * right2) / 2
        s0 = 1 - s + e * y * c2
        x0 = x + e * y * A2
        assert s0 >= 0
        assert left2 * s0 <= x0 <= right2 * s0
        checks.append(
            {
                "name": name,
                "lower_cell": i,
                "t0": str(t0),
                "upper_cell": jcell,
                "s0": str(s0),
            }
        )
    return checks


def geometry_sample(e=F(13, 125), n=10000, indices=(0, 1, 4999, 5000, 9999, 10000, 19999)):
    a = F(1, n)
    mstar = 1 + e * e + F(9, 16) * e**4
    k0 = mstar * (e + e * e / 2) + 2 * e * e
    delta = (k0 * a + mstar * e * e * a * a / 2) / (1 - e)

    def dot(u, v):
        return u[0] * v[0] + u[1] * v[1] + 2 * u[2] * v[2]

    rows = []
    for index in indices:
        family, j = divmod(index, n)
        left = -1 + 2 * j * a
        right = left + 2 * a
        center = (left + right) / 2
        secant = (1 + left * right) / 2
        q = max(abs(left), abs(right))
        cap = 1 + e * e * (q * q + q**4) / 2 + F(9, 16) * e**4 + delta
        t = cap / 2
        if family == 0:
            axis = (F(1), e * secant, e * center)
            verts = [(F(0), F(0), F(0)), (F(0), left * t, t), (F(0), right * t, t)]
        else:
            axis = (-e * secant, F(1), e * center)
            verts = [(F(0), F(0), F(1)), (left * t, F(0), 1 - t), (right * t, F(0), 1 - t)]
        nsq = dot(axis, axis)
        proj = []
        for v in verts:
            ratio = dot(v, axis) / nsq
            proj.append(tuple(x - ratio * y for x, y in zip(v, axis)))
        dots = [dot(p, axis) for p in proj]
        e1 = tuple(proj[1][k] - proj[0][k] for k in range(3))
        e2 = tuple(proj[2][k] - proj[0][k] for k in range(3))

        def phys_cross_norm2(u, w):
            c0 = u[1] * w[2] - u[2] * w[1]
            c1 = u[2] * w[0] - u[0] * w[2]
            c2 = u[0] * w[1] - u[1] * w[0]
            return 2 * c0 * c0 + 2 * c1 * c1 + c2 * c2

        area2 = phys_cross_norm2(e1, e2)
        rows.append(
            {
                "index": index,
                "nondeg": area2 > 0,
                "t_pos": t > 0,
                "perp": all(d == 0 for d in dots),
            }
        )
    return rows, delta


def main():
    print("=== polynomial identity (11) ===")
    diff = identity_difference()
    print("difference monomials:", len(diff), "ZERO" if not diff else "NONZERO")
    if diff:
        print(list(diff.items())[:8])

    e = F(13, 125)
    print("e", e, "e>1/10", e > F(1, 10), "1-e", 1 - e, "weights>0", 1 - e > 0)

    print("=== area isqrt (full N cells, independent) ===")
    new = area_bounds(F(13, 125))
    old = area_bounds(F(1, 10))
    print("new ints", new["lower_int"], new["upper_int"])
    print("old ints", old["lower_int"], old["upper_int"])
    print("new.upper < 4999213/1e7", new["upper"] < R13)
    print("old.lower > 4999215/1e7", old["lower"] > R15)
    print("new.upper < old.lower", new["upper"] < old["lower"])
    print("new.upper < threshold", new["upper"] < THRESH)

    print("=== Taylor/power-sum evenness bounds ===")
    tnew = taylor_half_sum(F(13, 125))
    told = taylor_half_sum(F(1, 10))
    print("T new upper < 4999213/1e7", tnew["upper"] < R13, tnew["upper"])
    print("T old lower > 4999215/1e7", told["lower"] > R15, told["lower"])
    print(
        "isqrt new inside Taylor",
        tnew["lower"] <= new["lower"] and new["upper"] <= tnew["upper"],
    )
    print(
        "isqrt old inside Taylor",
        told["lower"] <= old["lower"] and old["upper"] <= told["upper"],
    )

    print("=== first-crossing at vertices, e=13/125 ===")
    for row in first_crossing_endpoints():
        print(row)

    print("=== geometry sample ===")
    rows, delta = geometry_sample()
    print("delta", delta)
    for row in rows:
        print(row)
        assert row["nondeg"] and row["t_pos"] and row["perp"]

    claimed_new_lo = 4999212211665836198151146
    claimed_old_lo = 4999215859970016769600378
    print("match claimed new", new["lower_int"] == claimed_new_lo)
    print("match claimed old", old["lower_int"] == claimed_old_lo)

    a = F(1, N)
    for ee, name in [(F(13, 125), "new"), (F(1, 10), "old")]:
        mstar = 1 + ee * ee + F(9, 16) * ee**4
        d = F(2, N)
        delta5 = (
            d
            * (mstar * (ee + ee * ee / 2) + 2 * ee * ee + mstar * ee * ee * d / 4)
            / (2 * (1 - ee))
        )
        k0 = mstar * (ee + ee * ee / 2) + 2 * ee * ee
        delta_lead = (k0 * a + mstar * ee * ee * a * a / 2) / (1 - ee)
        print(name, "delta5==lead", delta5 == delta_lead)

    ok_area = new["upper"] < R13 < R15 < old["lower"] and new["upper"] < THRESH
    print("PASS_AREA" if ok_area else "FAIL_AREA")
    print("PASS_IDENTITY" if len(diff) == 0 else "FAIL_IDENTITY")


if __name__ == "__main__":
    main()
