"""
classify_patterns.py

For each parameter pair (x, y) in our enumerated set, classifies admissible
patterns into three regimes (Definition 4 of the preprint):

  - periodic of order r: sigma = B^r for some r | gcd(x, y), r >= 2
  - sporadic: primitive period y, but contained in some A_p with p | (2^x - 3^y)
  - irreducible (only when gcd(x, y) = 1): all patterns are sporadic

Reports the count of patterns in each regime, broken down by prime divisor of
2^x - 3^y.

Author: Oriol Corcoll Arias, 2026
License: MIT
"""
import csv
import os
from itertools import combinations
from math import gcd
from sympy import factorint


def cycle_value(period):
    y = len(period)
    S = [0]
    for a in period:
        S.append(S[-1] + a)
    return sum(3 ** (y - 1 - k) * 2 ** S[k] for k in range(y))


def compositions(x, y):
    for cuts in combinations(range(1, x), y - 1):
        prev = 0
        comp = []
        for c in cuts:
            comp.append(c - prev)
            prev = c
        comp.append(x - prev)
        yield tuple(comp)


def primitive_period(p):
    n = len(p)
    for d in range(1, n + 1):
        if n % d == 0:
            block = p[:d]
            if all(p[i] == block[i % d] for i in range(n)):
                return d
    return n


def classify(x, y, max_n=10**8):
    """
    Returns a dict with classification statistics.
    """
    diff = 2 ** x - 3 ** y
    if diff <= 0:
        return None
    fact = factorint(diff)
    primes = sorted(fact.keys())
    g = gcd(x, y)
    is_irreducible = (g == 1)

    n_total = 0
    A_p = {p: [] for p in primes}
    A_diff = []

    for sigma in compositions(x, y):
        n_total += 1
        if n_total > max_n:
            return None
        C = cycle_value(sigma)
        for p in primes:
            if C % p == 0:
                A_p[p].append(sigma)
        if C % diff == 0:
            A_diff.append(sigma)

    # For each A_p, classify patterns
    classification = {}
    for p, A in A_p.items():
        n_periodic = 0
        n_sporadic = 0
        for sigma in A:
            pp = primitive_period(sigma)
            if pp < y:
                n_periodic += 1
            else:
                n_sporadic += 1
        classification[p] = {
            "total": len(A),
            "periodic": n_periodic,
            "sporadic": n_sporadic,
        }

    return {
        "x": x, "y": y,
        "gcd": g,
        "is_irreducible": is_irreducible,
        "diff": diff,
        "factorisation": dict(fact),
        "n_total": n_total,
        "n_full_zero": len(A_diff),
        "by_prime": classification,
    }


CASES = [
    (4, 2), (6, 3), (8, 5), (10, 5), (10, 6), (12, 6), (12, 7),
    (14, 8), (16, 9), (16, 10),
    (20, 12), (22, 13), (24, 15), (25, 15), (26, 16), (27, 16), (27, 17),
]
# (29, 18), (31, 19), (32, 20), (34, 21), (35, 22) - too large for this pattern-by-pattern script


def main():
    rows = []
    print(f"{'(x,y)':>8} | {'gcd':>3} | {'class':>4} | "
          f"{'p':>10} | {'|A_p|':>8} | {'periodic':>8} | {'sporadic':>8}")
    print("-" * 75)

    for x, y in CASES:
        result = classify(x, y)
        if result is None:
            print(f"  ({x:>2},{y:>2}): SKIPPED (too large)")
            continue
        cls = "irr" if result["is_irreducible"] else f"r={result['gcd']}"
        first = True
        for p, stats in result["by_prime"].items():
            if first:
                print(f"  ({x:>2},{y:>2}) | {result['gcd']:>3} | {cls:>4} | "
                      f"{p:>10} | {stats['total']:>8} | "
                      f"{stats['periodic']:>8} | {stats['sporadic']:>8}")
                first = False
            else:
                print(f"  {'':>14} | {'':>4} | "
                      f"{p:>10} | {stats['total']:>8} | "
                      f"{stats['periodic']:>8} | {stats['sporadic']:>8}")
            rows.append({
                "x": x, "y": y, "gcd": result["gcd"],
                "class": cls, "prime": p,
                "A_p_size": stats["total"],
                "periodic": stats["periodic"],
                "sporadic": stats["sporadic"],
            })

    # Write CSV
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(repo_root, "data", "classification.csv")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x", "y", "gcd", "class", "prime", "A_p_size",
                    "periodic_count", "sporadic_count"])
        for r in rows:
            w.writerow([r["x"], r["y"], r["gcd"], r["class"], r["prime"],
                        r["A_p_size"], r["periodic"], r["sporadic"]])
    print()
    print(f"Wrote {csv_path}")


if __name__ == "__main__":
    main()
