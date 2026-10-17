# A smaller-area 20,000-cylinder cover of the regular tetrahedron

[Read the paper](paper.pdf) · [LaTeX source](main.tex) · [Exact comparison](COMPARISON.md)

We refine the compatible-secant construction with **e = 13/125** and
**N = 10,000**, obtaining a cover of the closed regular tetrahedron by
**20,000 triangular cylinders** with normalized total base area

```text
R_new < 0.4999213 < 0.4999215 < R_old.
```

Here `R_old` is the actual area of the published `e=1/10`, `N=10000` instance.
The improvement is approximately **3.6483 × 10⁻⁷** at the same cylinder count.
The comparison permits the cylinder axes to vary with the parameter `e`.

## Construction and proof

The body is

```text
K = {(x,y,sqrt(2)s): 0 <= s <= 1, |x| <= 1-s, |y| <= s}.
```

Each cylinder has a compact nondegenerate triangular base perpendicular to its
axis. Total base area is normalized by the tetrahedron's minimum projection
area `sqrt(2)`. The proof covers the entire closed body, including its boundary,
and establishes the geometric construction for `0<e<1`.

The finite-area comparison is certified by integer-square-root enclosures and
independent rational Taylor/power-sum bounds.

## Reproduce

Python 3.8+ and its standard library are sufficient. Run without `-O`:

```sh
python3 code/reproduce.py
python3 code/retuned_secants.py --index 0
python3 code/retuned_secants.py --index 19999
```

The first command checks all 10,000 summands for each parameter, the overlap
identity and the strict area comparison. The constructor returns rational axes
and vertices in `(x,y,z/sqrt(2))` coordinates, with physical metric
`diag(1,1,2)`.

Build the paper with TeX Live and latexmk:

```sh
latexmk -pdf -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
```

## Materials

- `paper.pdf`, `main.tex`, `references.bib`: proof and references.
- `code/`: exact constructor and reproduction program.
- `checkers/`: independent checks and rational certificates.
- `COMPARISON.md`, `ATTRIBUTION.md`: benchmark, scope and source credits.
- `result.json`: precise statement and verification record.

Verification at this release consists of automated proof review and reproduced
exact-arithmetic checks. Independent mathematical review is welcome.

## Acknowledgments and Euler

OpenAI supplies the angular/secant framework and first-crossing argument.
The [shjvandekamp construction](https://github.com/shjvandekamp/math/tree/main/topics/cylinder-covering)
supplies the quartic cap, overlap identity and finite padding. This work adds
the parameter refinement and its exact finite-area certificate.

The work was developed through collaboration between **Astra and GPT-6.1 Sol**
within **Euler**, a mathematical research agent framework with a shared proof
graph and interactive research workflow. We welcome researchers to try it.

**Code:** https://github.com/canghaimeng/Euler

**Website:** https://canghaimeng.site/euler/?lang=zh
