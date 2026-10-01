import numpy as np, matplotlib.pyplot as plt
k, n = map(int, input().split())
a = np.random.randint(-10, 11, (n, n))
h = n // 2
print('a\n', a)
f = a.copy()
e = f[h:, h:]
fl = np.sum(e[:, ::2] > k) > np.prod(e[1::2, :]) if e[1::2, :].size else False
if fl: f[:h, h:], f[h:, h:] = e.T.copy(), f[:h, h:].T.copy()
else:   f[:h, h:], f[:h, :h] = a[:h, :h].copy(), a[:h, h:].copy()
print('f\n', f)
res = a @ a.T - k * np.linalg.inv(f) if np.linalg.det(a) > np.trace(f) else (np.linalg.inv(a) + np.tril(a) - f.T) * k
print('res\n', np.round(res, 2))

fig, ax = plt.subplots(1, 3, figsize=(15, 4))
ax[0].imshow(a, cmap="RdBu_r", vmin=-10, vmax=10); ax[0].set_title("a"); plt.colorbar(ax[0].images[0], ax=ax[0])
ax[1].imshow(f, cmap="RdBu_r", vmin=-10, vmax=10); ax[1].set_title("f"); plt.colorbar(ax[1].images[0], ax=ax[1])
ax[2].bar(np.arange(n) - .2, np.diag(a), .4, label="diag a", color="steelblue")
ax[2].bar(np.arange(n) + .2, np.diag(f), .4, label="diag f", color="tomato"); ax[2].legend(); ax[2].set_title("диагонали")
plt.tight_layout(); plt.savefig("matrix.png", dpi=150); plt.show()
