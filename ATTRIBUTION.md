# Dated source comparison

Cutoff: 17 October 2026 (UTC date). The audit includes the supplied source pack,
primary repository revisions, and targeted browser searches. It is not an
exhaustive priority search. Primary URLs, retrieval times and source hashes appear below. The exact accepted
statement and reproduction metadata are in result.json.

## Fixed model

K = {(x,y,sqrt(2)s): 0 <= s <= 1, |x| <= 1-s, |y| <= s}.
The denominator is the minimum Euclidean projection area A_min(K)=sqrt(2).
Cylinders are infinite, with compact nondegenerate triangular bases in their
axis-perpendicular planes. Sum areas with multiplicity. Coverage includes all
boundary points. The current target has at most 20000 cylinders and no separate
axis-angle restriction.

## Original OpenAI result

The displayed theorem of Finite angular cylinder covers below the half-area
bound (27 September 2026), at OpenAI revision
1581d4cbdd69a0faf34b2089614fe2a814316a6a, gives

    m = 2 ceil(2/epsilon^2), 0 < epsilon <= 1/2000,
    R = 1/2 - (13/6000) epsilon^2 + E, |E| <= 2 epsilon^4.

The explicit epsilon=1/2000 instance uses 16000000 cylinders and has actual
area at least 1/2 - 13/(6000*2000^2) - 2/2000^4 > 0.4999215.
The supplied code/reproduce.py checks that rational comparison. Our 20000-cylinder
instance improves both count and area for that explicit realization and
quantifies the original below-half conclusion.

The four original manuscripts are acknowledged. We do not claim that every
admissible parameter choice in every OpenAI family is worse. That would require
additional comparisons beyond the displayed theorem and the checked benchmark.

## Strongest checked public same-budget benchmark

Van de Kamp's A quartic overlap theorem with effective finite secant covers
(15 October 2026), pinned at db6e1d89a0637b013a86464bd766c0a5120e454e, supplies
the quartic cap, finite secant padding, and closed-body proof. At e=1/10 and
N=10000 it reports

    0.499921585997001674 <= R_old <= 0.499921585997001774.

The closed-set proof is reproduced in this package rather than adopted as an
unchecked premise. Two independent exact methods recompute the actual finite
sum. The sharper integer enclosure obtained here is

    0.4999215859970016769600378 <= R_old
      < 0.4999215859970016769610378.

The latest inspected topic-changing revision
8b63303107ca07dce2e72ed65b11d3af75540e5f (15 October 2026, 18:28:10 UTC)
retains this numerical benchmark. It reports Lean formalization; that build was
not rerun locally and is not used as a premise or claimed as our certification.

Our new parameter choice e=13/125, N=10000 gives

    0.4999212211665836198151146 <= R_new
      < 0.4999212211665836198161146.

Thus this is a different set of axes and caps with strictly smaller actual
area, not re-rounding the published example. Geometry and padding are credited
to the original authors. The new tilt is larger; the original source's
same-angle comparisons cannot be automatically extended.

## Other public claims checked for relevance

The Lattice/Fixpoint family-100 card in the public new_math_review showcase
(8 October 2026; pinned cd6549b24054e6869f480f598f314f263b27e6cf) reports a
1000000-cylinder instance with saving at least 2959/5187500000000 below 1/2.
The page also reports counts 933156 and 929752 at the edge of its sufficient
parameter window. All exceed 20000. Its displayed upper bound is weaker
than the checked van de Kamp benchmark. This audit checks the reported claim's
scope and comparison; it does not independently reproduce that entire proof.

The current van de Kamp result note also records an earlier 20000-cylinder
radial construction in [0.499947504745824,0.499947504745984] and a
40000-cylinder e=1/100,N=20000 secant instance near 0.499998863418315728.
Those reported costs do not improve the chosen benchmark. Their specialized
optimality claims concern restricted classes, not all tetrahedron covers.

## Comparison scope

The numerical comparison covers the explicitly identified constructions above,
with the tetrahedron, normalized area and cylinder count fixed as stated.
The parameter refinement has a larger maximum axis tilt. The source search
cutoff is 17 October 2026. Exact verification details are recorded in result.json.

## Source provenance

The targeted source search completed at 2026-10-17T05:49:25.841189Z; its date
cutoff is 17 October 2026. The following immutable source snapshots were
retrieved again for byte-level citation checks while packaging. Retrieval
of a pinned snapshot is separate from a new search for later results.
The original and secant manuscript bytes match the previously inspected copies.
Hashes identify the complete retrieved artifact named by each URL; the public
showcase comparison uses only its family-100 entry.

- [Finite angular cylinder covers below the half-area bound, displayed theorem](https://raw.githubusercontent.com/openai/math/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Finite-angular-cylinder-covers-below-the-half-area-bound-September-27-2026/build/sections/introduction.tex)
  - Retrieved: 2026-10-17T07:01:52Z
  - SHA256: `19c5b71d779403be3fd80bca70cfa2414d4a10286a0743e51fcb894fa309841d`

- [A quartic overlap theorem with effective finite secant covers](https://raw.githubusercontent.com/shjvandekamp/math/db6e1d89a0637b013a86464bd766c0a5120e454e/topics/cylinder-covering/SECANT-THEOREM.md)
  - Retrieved: 2026-10-17T07:03:49Z
  - SHA256: `8bd207b80ea0d4596c7b211a47862eafe4c38c4dba3d73f1e74e421afcea0d75`

- [Result: an effective quartic/secant cover of the regular tetrahedron](https://raw.githubusercontent.com/shjvandekamp/math/8b63303107ca07dce2e72ed65b11d3af75540e5f/topics/cylinder-covering/RESULT.md)
  - Retrieved: 2026-10-17T07:01:50Z
  - SHA256: `6a98c9f502120df594b8a4b6fade62f3df640c978e55ce9f8fd712d3ccb85d58`

- [A quartic overlap theorem with effective finite secant covers, later inspected revision](https://raw.githubusercontent.com/shjvandekamp/math/8b63303107ca07dce2e72ed65b11d3af75540e5f/topics/cylinder-covering/SECANT-THEOREM.md)
  - Retrieved: 2026-10-17T07:03:51Z
  - SHA256: `696870a343cda2e5a1e5250429522b3fe04e41442428d071583df3a9a2e7eb7a`

- [Covering a tetrahedron with a million thin cylinders, public showcase entry](https://raw.githubusercontent.com/supsup/new_math_review/cd6549b24054e6869f480f598f314f263b27e6cf/showcase.md)
  - Retrieved: 2026-10-17T07:03:53Z
  - SHA256: `21c167d73506296501d613c0a0a193c3200672c4b215431f277221023ea9fd52`

## Bibliographic metadata

The four OpenAI bibliographic records were read from their publisher-supplied
README files at revision 1581d4cbdd69a0faf34b2089614fe2a814316a6a. The hashes
below apply to those metadata files, not to the linked manuscripts' PDF bytes.

- [Finite angular cylinder covers below the half-area bound: publisher metadata](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Finite-angular-cylinder-covers-below-the-half-area-bound-September-27-2026/README.md) — SHA256 `eea889085336a9626a1682f8b862d6e9b0f48fc10ab9690850a63f6464112e20`.
- [Finite cylinder approximation of ruled sets: publisher metadata](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Finite-cylinder-approximation-of-ruled-sets-September-27-2026/README.md) — SHA256 `468fa04859ad9a0d2310604e5146f41bce53e7be724a3b1880880dade7b93a0a`.
- [Slope-field perturbations of the two-cylinder covering: publisher metadata](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Slope-field-perturbations-of-the-two-cylinder-covering-September-27-2026/README.md) — SHA256 `a29a0ea828b1204dce0766ac1b261e188c333c34b9b7dcdfe4beca3d09e43054`.
- [Finite triangular approximation of radial sweeps: publisher metadata](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Finite-triangular-approximation-of-radial-sweeps-September-27-2026/README.md) — SHA256 `af80de9cf252318ca91134d5cd0ad4b5a48824307de654273c20318a70ea626f`.

The secant/result manuscripts are credited to their public repository account,
shjvandekamp. No personal initials are inferred. Lattice and Fixpoint are the
names displayed by the cited public showcase; its reported verification is
not adopted as a premise of the proof here. All cited results are used only
within the scope described above.
