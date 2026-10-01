def alg_pairs(n):
    pairs = []
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            pairs.append((i,j))
        return pairs
print(alg_pairs(3))
