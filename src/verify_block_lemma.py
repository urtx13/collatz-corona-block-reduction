"""
verify_block_lemma.py

Verifies Lemma 1 (block reduction) and the algebraic factorisation
2^x - 3^y = (2^a - 3^b) * Phi_{a, b, r} of Proposition 2 numerically.

For random base blocks B and random orders r, checks the integer identity

    C(y, B^r) = C(b, B) * Phi_{a, b, r}

where x = r*a, y = r*b, a = sum(B), b = len(B), and
Phi = sum_{j=0..r-1} 2^{j*a} * 3^{(r-1-j)*b}.

Also verifies the three illustrated cases from the preprint:
  Case 1: (24, 15) with r = 3, (a, b) = (8, 5)
  Case 2: (16, 10) with r = 2, (a, b) = (8, 5)
  Case 3: (26, 16) with r = 2, (a, b) = (13, 8)

Author: Oriol Corcoll Arias, 2026
License: MIT
"""
import random
from itertools import combinations
from math import gcd
from sympy import factorint


def cycle_value(period):
    """C(y, sigma) = sum_{k=0}^{y-1} 3^{y-1-k} * 2^{S_k}."""
    y = len(period)
    S = [0]
    for a in period:
        S.append(S[-1] + a)
    return sum(3 ** (y - 1 - k) * 2 ** S[k] for k in range(y))


def Phi(a, b, r):
    """Phi_{a, b, r} = sum_{j=0..r-1} 2^{j*a} * 3^{(r-1-j)*b}."""
    return sum(2 ** (j * a) * 3 ** ((r - 1 - j) * b) for j in range(r))


def compositions(x, y):
    """All compositions of x into y parts >= 1."""
    for cuts in combinations(range(1, x), y - 1):
        prev = 0
        comp = []
        for c in cuts:
            comp.append(c - prev)
            prev = c
        comp.append(x - prev)
        yield tuple(comp)


def test_block_identity(B, r):
    """Verify C(y, B^r) = C(b, B) * Phi_{a, b, r}."""
    sigma = tuple(B) * r
    a, b = sum(B), len(B)
    C_full = cycle_value(sigma)
    C_block = cycle_value(B)
    phi = Phi(a, b, r)
    return C_full == C_block * phi, C_full, C_block, phi


def test_diff_factorisation(a, b, r):
    """Verify 2^(r*a) - 3^(r*b) = (2^a - 3^b) * Phi_{a, b, r}."""
    diff_full = 2 ** (r * a) - 3 ** (r * b)
    diff_block = 2 ** a - 3 ** b
    phi = Phi(a, b, r)
    return diff_full == diff_block * phi, diff_full, diff_block, phi


# -----------------------------------------------------------------------------
# Random tests
# -----------------------------------------------------------------------------

def random_tests(n_trials=20):
    print("=" * 70)
    print("Random verification of the block identity")
    print("=" * 70)
    print()
    print(f"{'B':>30} | {'r':>2} | {'identity holds':>15}")
    print("-" * 60)
    random.seed(42)
    fails = 0
    for _ in range(n_trials):
        b = random.randint(2, 8)
        a_target = random.randint(b + 1, 3 * b)  # ensure 2^a > 3^b
        # generate random composition of a into b parts
        cuts = sorted(random.sample(range(1, a_target), b - 1))
        prev = 0
        B = []
        for c in cuts:
            B.append(c - prev)
            prev = c
        B.append(a_target - prev)
        r = random.randint(2, 4)
        ok, _, _, _ = test_block_identity(B, r)
        print(f"  {str(B):>30} | {r:>2} | {'OK' if ok else 'FAIL':>15}")
        if not ok:
            fails += 1
    print()
    print(f"Trials: {n_trials}, failures: {fails}")
    print()


# -----------------------------------------------------------------------------
# Featured cases
# -----------------------------------------------------------------------------

def featured_cases():
    print("=" * 70)
    print("Featured cases (Section 4.2 of the preprint)")
    print("=" * 70)

    cases = [
        ("(x, y) = (24, 15), r=3", 24, 15, 3, 8, 5),
        ("(x, y) = (16, 10), r=2", 16, 10, 2, 8, 5),
        ("(x, y) = (26, 16), r=2", 26, 16, 2, 13, 8),
    ]

    for name, x, y, r, a, b in cases:
        print()
        print(f"--- {name}, (a, b) = ({a}, {b}) ---")

        # Verify diff factorisation
        diff_full = 2 ** x - 3 ** y
        diff_block = 2 ** a - 3 ** b
        phi = Phi(a, b, r)
        assert diff_full == diff_block * phi
        print(f"  2^{x} - 3^{y} = {diff_full}")
        print(f"               = (2^{a} - 3^{b}) * Phi_{{a,b,r}}")
        print(f"               = {diff_block} * {phi}")
        print(f"  factorisation of 2^{a} - 3^{b}:    {dict(factorint(diff_block))}")
        print(f"  factorisation of Phi:              {dict(factorint(phi))}")
        print(f"  gcd(2^{a}-3^{b}, Phi) = {gcd(diff_block, phi)}")

        # Enumerate all blocks and count cycle integrality
        n_blocks = 0
        n_block_div_diff_block = 0
        n_full_div_phi = 0
        n_full_div_full = 0

        for B in compositions(a, b):
            n_blocks += 1
            sigma = tuple(B) * r

            C_block = cycle_value(B)
            C_full = cycle_value(sigma)

            # Algebraic check
            if C_full != C_block * phi:
                print(f"  ALGEBRAIC FAILURE for B = {B}!")
                continue

            # Forced divisibility by Phi
            if C_full % phi == 0:
                n_full_div_phi += 1

            # Reduces to: (2^a - 3^b) | C(b, B)
            if C_block % diff_block == 0:
                n_block_div_diff_block += 1
                # Should also have full divisibility
                if C_full % diff_full == 0:
                    n_full_div_full += 1

        print(f"  blocks enumerated: {n_blocks}")
        print(f"  blocks with (2^a - 3^b) | C(b, B):  {n_block_div_diff_block}")
        print(f"  patterns B^r with Phi | C(y, B^r):  {n_full_div_phi}")
        print(f"  ==> all {n_blocks} patterns B^r have Phi | C(y, B^r)? "
              f"{n_full_div_phi == n_blocks}")
        print(f"  patterns B^r with (2^x - 3^y) | C(y, B^r): {n_full_div_full}")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    random_tests()
    featured_cases()
