import timeit, sys, math

def rec(n):
    if n <= 2: return 1
    zn = 1 if n % 2 == 0 else -1
    return zn * (rec(n-2) / math.factorial(2*n))

def itr(n):
    a, b, fact = 1.0, 1.0, 24.0
    if n <= 2: return 1
    for i in range(3, n+1):
        zn = 1 if i % 2 == 0 else -1
        fact *= (2*i-1) * (2*i)
        val = zn * a / fact
        a, b = b, val
    return b


def main():
    sys.setrecursionlimit(10000)
    max_rec = 0
    max_itr = 0
    
    for n in range(1, 50):
        try:
            rec(n)
            max_rec = n
        except RecursionError:
            break
    
    for n in range(1, 500):
        try:
            itr(n)
            max_itr = n
        except (OverflowError):
            break
 
    print(f"Границы:")
    print(f"Рекурсия: n <= {max_rec}")
    print(f"Итерация: n <= {max_itr}")
    print(f"\n{'n':>3}  {'Рекурсия ':>15}  {'Итерация ':>15}  {'Ускорение':>10}")
    
    test_limit = min(max_rec, 25)
    
    for n in range(2, test_limit + 1):
        if n <= max_rec:
            try:
                t_rec = min(timeit.repeat(lambda n=n: rec(n), number=100, repeat=2)) / 100
            except:
                t_rec = float('inf')
        else:
            t_rec = float('inf')
        
        try:
            t_itr = min(timeit.repeat(lambda n=n: itr(n), number=10000, repeat=3)) / 10000
        except:
            t_itr = float('inf')
        
        if t_rec == float('inf'):
            print(f"{n:3d}  {'ошибка':>15}  {t_itr:15.8f}  {'---':>10}")
        elif t_itr == float('inf'):
            print(f"{n:3d}  {t_rec:15.8f}  {'ошибка':>15}  {'---':>10}")
        else:
            speedup = t_rec / t_itr
            print(f"{n:3d}  {t_rec:15.8f}  {t_itr:15.8f}  {speedup:10.2f}")
    
if __name__ == "__main__":
    main()
