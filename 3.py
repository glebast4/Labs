def check(i, j):
    if (i == j) or (i + j == n - 1):
        return 0
    if (j < i) and (i + j < n - 1):
        return 1
    if (j > i) and (i + j < n - 1):
        return 2
    if (j > i) and (i + j > n - 1):
        return 3
    else:
        return 4

def printm(m):
    for i in m:
        print(" "+" ".join(f"{x:5}" for x in i))
    print()
    
def trans(x):
    return [[x[j][i] for j in range(n)] for i in range(n)]

def mul(x, y):
    return [[sum(x[i][k] * y[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

k, n = map(int, input().split())
a = []

with open("matr.txt") as f:
        for i in f:
            a.append(list(map(int, i.split())))

printm(a)

z = 0
s = 0
for i in range(n):
    for j in range(n):
        if check(i, j) == 3 and j  % 2 != 0 and a[i][j] == 0:
            z += 1
        if check(i, j) == 1 and (i + 1) % 2 == 0:
            s += a[i][j]
print("Нули в нечетных столбцах в 3:", z)
print("Сумма в четных строкак в 1:", s, '\n')

f = [h[:] for h in a]
if z > s:
    #меняю 2 и 3 сим
    for i in range(n):
        for j in range(n):
            if check(i, j) == 2:
                f[i][j], f[n-1-i][n-1-j] = a[n-1-i][n-1-j], a[i][j]
else:
    #меняю 3 и 4 несим
    r3 = [(i, j) for i in range(n) for j in range(n) if check(i, j) == 3]
    r4 = [(i, j) for i in range(n) for j in range(n) if check(i, j) == 4]
    for x in range(min(len(r3), len(r4))):
        i3, j3 = r3[x]
        i4, j4 = r4[x]
        f[i3][j], f[i4][j4] = a[i4][j4], a[i3][j3]

printm(f)

af = mul(a, f)
printm(af)

ft = trans(f)
printm(ft)

kft = [[k*ft[i][j] for j in range(n)] for i in range(n)]
printm(kft)

res = [[af[i][j] - kft[i][j] for j in range(n)] for i in range(n)]
printm(res)

