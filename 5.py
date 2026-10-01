import sys, time, math
from functools import lru_cache

def exponent(n, prev): #логарифмическое решение (2n!)
    if prev == 0.0: return 0.0
    res = math.log(n) + math.log(abs(prev)) - math.lgamma(2 * n + 1)
    return 0.0 if res < -700 else math.copysign(math.exp(res), prev)

def neg(x): #формула Эйлера (-1)^n
    return math.cos(math.pi * x)

@lru_cache(maxsize=None)
def rec(n):
    return 1.0 if n <= 2 else neg(exponent(n, rec(n - 2)))

def itr(n):
    if n <= 2: return 1.0
    a, b = 1.0, 1.0
    for i in range(3, n + 1):
        a, b = b, neg(exponent(i, a))
    return b

def bench(fn, n, k = 500):
    t = time.perf_counter()
    for i in range(k):
        if hasattr(fn, 'cache_clear'): fn.cache_clear()
        fn(n)
    return (time.perf_counter() - t) / k * 1e6

def main():
    sys.setrecursionlimit(10_000)
    L = [1, 2, 3, 4, 5, 10, 20, 50, 100, 500, 1000]
    lim = (sys.getrecursionlimit() - 100) * 2

    print(f"\n{'n':>5} {'F_rec':>12} {'F_itr':>12} {'t_rec':>10} {'t_itr ':>10}")

    for n in L:
        ti = bench(itr, n)
        vi = itr(n)
        if n <= lim:
            tr = bench(rec, n)
            rec.cache_clear();
            vr = rec(n)
            print(f"{n:>5} {vr:>12.6f} {vi:>12.6f} {tr:>10.2f} {ti:>10.2f}")
        else:
            print(f"{n:>5} {'стек!':>12} {vi:>12.6f} {'—':>10} {ti:>10.2f}")

    print(f"\nРекурсия: n <= {lim}  (глубина стека - n/2,  память O(n))")
    print("Итерация: n не ограничен (три переменные, память O(1))\n")

if __name__ == "__main__":
    main()






