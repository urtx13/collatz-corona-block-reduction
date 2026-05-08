# Block Reduction and Mutual Exclusion in the Collatz Corona

Working research note and reproducibility archive.

## Summary

This repository accompanies the working draft:

**Block Reduction and Mutual Exclusion in the Collatz Corona**  
Oriol Corcoll Arias, May 2026.

The note studies the cyclic component of the accelerated Collatz map through the Collatz corona, following the cycle-equation framework of Böhm--Sontacchi, Lagarias, and Belaga--Mignotte.

The main contribution is an exact block-factorisation identity. If \(x=ra\), \(y=rb\), and an admissible exponent pattern is an \(r\)-fold repetition \(B^r\) of a base block \(B\in\Sigma(a,b)\), then

$$
C(rb,B^r)=C(b,B)\Phi_{a,b,r},
$$

where

$$
\Phi_{a,b,r}=\sum_{j=0}^{r-1}2^{ja}3^{(r-1-j)b}.
$$

At the same time,

$$
2^{ra}-3^{rb}=(2^a-3^b)\Phi_{a,b,r}.
$$

Therefore, on the periodic stratum of the Collatz corona, the cycle integrality condition at \((x,y)\) reduces exactly to the corresponding condition for the smaller base pair \((a,b)\). No coprimality assumption is needed for this global reduction.

The note does **not** prove the Collatz conjecture or the absence of non-trivial cycles. It isolates a structural mechanism for periodic patterns and leaves two regimes open: sporadic primitive patterns in reducible parameter pairs and irreducible parameter pairs with \(\gcd(x,y)=1\).

## Repository structure

    .
    ├── README.md
    ├── LICENSE
    ├── paper/
    │   └── preprint.tex
    ├── src/
    │   ├── verify_block_lemma.py
    │   └── classify_patterns.py
    ├── data/
    │   └── classification.csv
    └── results/
        └── classification_log.txt

## Main files

- `paper/preprint.tex` — LaTeX source of the working draft.
- `src/verify_block_lemma.py` — verification script for the block-factorisation identity.
- `src/classify_patterns.py` — classifier for periodic, sporadic, and irreducible cases.
- `data/classification.csv` — per-case classification table.
- `results/classification_log.txt` — readable classification output.

## Featured reductions

### \((x,y)=(24,15)\)

$$
24=3\cdot 8,\qquad 15=3\cdot 5.
$$

$$
2^{24}-3^{15}
=
(2^8-3^5)(2^{16}+2^8 3^5+3^{10})
=
13\cdot 186793.
$$

For every \(B\in\Sigma(8,5)\),

$$
C(15,B^3)=186793\,C(5,B).
$$

Thus the global cycle condition for repeated blocks \(B^3\) reduces to

$$
13\mid C(5,B).
$$

### \((x,y)=(16,10)\)

$$
16=2\cdot 8,\qquad 10=2\cdot 5.
$$

$$
2^{16}-3^{10}
=
(2^8-3^5)(2^8+3^5)
=
13\cdot 499.
$$

For every \(B\in\Sigma(8,5)\),

$$
C(10,B^2)=499\,C(5,B).
$$

Thus the global cycle condition for repeated blocks \(B^2\) reduces to

$$
13\mid C(5,B).
$$

### \((x,y)=(15,9)\)

$$
15=3\cdot 5,\qquad 9=3\cdot 3.
$$

$$
2^{15}-3^9
=
(2^5-3^3)(2^{10}+2^5 3^3+3^6)
=
5\cdot 2617.
$$

For every \(B\in\Sigma(5,3)\),

$$
C(9,B^3)=2617\,C(3,B).
$$

Thus the global cycle condition for repeated blocks \(B^3\) reduces to

$$
5\mid C(3,B).
$$

### \((x,y)=(26,16)\)

$$
26=2\cdot 13,\qquad 16=2\cdot 8.
$$

$$
2^{26}-3^{16}
=
(2^{13}-3^8)(2^{13}+3^8)
=
1631\cdot 14753
=
7\cdot 233\cdot 14753.
$$

For every \(B\in\Sigma(13,8)\),

$$
C(16,B^2)=14753\,C(8,B).
$$

Thus the global cycle condition for repeated blocks \(B^2\) reduces to

$$
1631\mid C(8,B).
$$

## Quick reproduction

Run:

    python3 src/verify_block_lemma.py
    python3 src/classify_patterns.py

## Status

This is a working draft. The block-factorisation identity is exact. The computational classification is finite and reproducible from the included scripts/data.

The note does not prove the Collatz conjecture. It does not prove the absence of non-trivial Collatz cycles. It gives an exact recursive reduction for periodic patterns in the Collatz corona and isolates the remaining obstruction in sporadic and irreducible regimes.

## Citation

    @misc{corcoll2026blockreduction,
      author = {Corcoll Arias, Oriol},
      title  = {Block Reduction and Mutual Exclusion in the Collatz Corona},
      year   = {2026},
      note   = {Working draft},
      url    = {https://github.com/urtx13/collatz-corona-block-reduction}
    }

## License

MIT. See `LICENSE`.
