# Block Reduction and Mutual Exclusion in the Collatz Corona

**Version 2** of the working draft and reproducibility archive.

## Summary

This is a substantial extension of the version 1 note (Zenodo, May 2026).
Version 2 isolates a rigorous algebraic mechanism behind the empirical
mutual-exclusion phenomenon recorded in version 1: a **block reduction
lemma** for the cycle constant, combined with the standard algebraic
factorisation `2^x - 3^y = (2^a - 3^b) * Phi_{a, b, r}` whenever
`gcd(x, y) >= 2`.

The lemma yields a recursive reduction of the cyclic obstruction within
**periodic patterns** (those of the form `B^r` for some block `B`), and
classifies admissible patterns into three regimes:

  - **Periodic** (covered by the lemma)
  - **Sporadic** (primitive period `y` within reducible parameter pairs)
  - **Irreducible** (parameter pairs with `gcd(x, y) = 1`)

The conjecture is reformulated as the conjunction of two unresolved
statements: one on sporadic patterns, one on irreducible base cases.

## Author

Oriol Corcoll Arias (working draft, May 2026).

## Repository structure

```
.
├── README.md                          this file
├── LICENSE                            MIT
├── HOW_TO_PUBLISH.md                  GitHub / Zenodo instructions
├── paper/
│   ├── preprint.tex                   LaTeX source
│   └── preprint.pdf                   compiled (6 pages)
├── src/
│   ├── enumerate_compositions.c       fast C enumerator (uint64, ~10^7 patterns/s)
│   ├── verify_block_lemma.py          NEW: rigorous test of Lemma 1 (preprint)
│   ├── classify_patterns.py           NEW: periodic / sporadic / irreducible classifier
│   ├── mutual_exclusion.py            marginal vs. joint analysis (v1)
│   └── verify_27_17.py                independent Python verification of (27, 17) (v1)
├── data/
│   ├── results_summary.csv            22 enumerated cases, totals
│   ├── mutual_exclusion_24_15.csv     per-factor breakdown of (24, 15)
│   └── classification.csv             NEW: pattern classification per case and prime
└── results/
    ├── log_runs.txt                   raw enumeration logs (large cases)
    └── classification_log.txt         NEW: classification table
```

## What is new in version 2

  1. **Lemma 1 (block reduction)** with full proof. For
     `sigma = B^r` with `x = r*a`, `y = r*b`,
     ```
     C(y, sigma) = C(b, B) * Phi_{a, b, r}
     ```
     as integers, where `Phi_{a, b, r} = sum_{j=0..r-1} 2^{j*a} * 3^{(r-1-j)*b}`.

  2. **Proposition 2 (factorisation)**. The algebraic identity
     `2^(r*a) - 3^(r*b) = (2^a - 3^b) * Phi_{a, b, r}`.

  3. **Corollary 4 (recursive reduction)**. Under coprimality
     `gcd(2^a - 3^b, Phi_{a, b, r}) = 1`,
     ```
     (2^x - 3^y) | C(y, B^r)  iff  (2^a - 3^b) | C(b, B).
     ```

  4. **Theorem 5 (recursive structure)**. Conjecture 6 holds for all
     reducible parameter pairs if it holds for irreducible parameter pairs
     and for sporadic patterns of reducible pairs.

  5. **Three featured cases** with full algebraic identification:
     - `(24, 15) = (3 * 8, 3 * 5)`: `186793 = Phi_{8, 5, 3}`
     - `(16, 10) = (2 * 8, 2 * 5)`: `499 = 2^8 + 3^5 = Phi_{8, 5, 2}`
     - `(26, 16) = (2 * 13, 2 * 8)`: `14753 = 2^13 + 3^8 = Phi_{13, 8, 2}`

  6. **Classification of all 22 tested cases** as irreducible / reducible
     and per-prime breakdown of periodic vs. sporadic patterns
     (`data/classification.csv`).

## Quick reproduction

```bash
# 1. Build the C enumerator
gcc -O3 -o enumerate_compositions src/enumerate_compositions.c

# 2. Verify the block lemma (random tests + featured cases)
python3 src/verify_block_lemma.py

# 3. Classify patterns by regime
python3 src/classify_patterns.py

# 4. Mutual exclusion analysis (v1, still relevant)
python3 src/mutual_exclusion.py

# 5. Independent Python verification of the (27, 17) critical case
python3 src/verify_27_17.py
```

## What is unchanged from version 1

The empirical observations (Table 1 of the preprint), the mutual
exclusion data at (24, 15), and the per-case enumeration logs.

The mutual exclusion observation now has a **partial algebraic
explanation** (via Corollary 3 + Corollary 4 of the preprint) that
was missing in version 1.

## Citation

```bibtex
@misc{corcoll2026blockv2,
  author = {Oriol Corcoll Arias},
  title  = {Block Reduction and Mutual Exclusion in the Collatz Corona, v2},
  year   = {2026},
  note   = {Working draft, supersedes Zenodo v1 (May 2026)},
  url    = {https://github.com/<USER>/collatz-mutual-exclusion}
}
```

## License

MIT. See `LICENSE`.
