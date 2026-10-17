# Public comparison — 17 October 2026

The public baseline at repository revision
`bc1a91860188a61e73ccca6dd1a6a34082dad59b` still displays the
`e=1/10`, `N=10000` compatible-secant cover:

```text
0.499921585997001674 <= R_old <= 0.499921585997001774.
```

Our `e=13/125`, `N=10000` instance satisfies the tighter exact enclosure

```text
4999212211665836198151146 / 10^25 <= R_new
R_new < 4999212211665836198161146 / 10^25.
```

The normalized-area decrease is approximately `3.6483e-7` at the same
20,000-cylinder count. These are areas of the actual finite constructions.
The comparison fixes the cylinder count and lets the axes vary with the
parameter; the new instance has a larger maximum axis tilt.

The original geometric method and finite padding are credited to the source.
Since `13/125 > 1/10`, the paper supplies coverage on its stated wider domain
and exact finite-area calculations for the selected parameter.

Baseline: [RESULT.md](https://github.com/shjvandekamp/math/blob/bc1a91860188a61e73ccca6dd1a6a34082dad59b/topics/cylinder-covering/RESULT.md).
Original theorem: [SECANT-THEOREM.md](https://github.com/shjvandekamp/math/blob/bc1a91860188a61e73ccca6dd1a6a34082dad59b/topics/cylinder-covering/SECANT-THEOREM.md).
