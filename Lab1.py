import math
import matplotlib.pyplot as plt

x = 42

def GenU():
    global x
    a, b, c = 16807, 0, 2147483647
    x = (a * x + b) % c
    return x / c

def Poisson(lam):
    X, S, q = -1, 1, math.exp(-lam)
    while S > q:
        S *= GenU()
        X += 1
    return X

def Gauss(mu, sigma):
    while True:
        U, V = GenU(), GenU() * (2 / math.e)
        X = V / U
        if X**2 <= -4 * math.log(U):
            return mu + X * sigma

p_dane = [Poisson(5) for _ in range(5000)]
g_dane = [Gauss(0, 1) for _ in range(5000)]

plt.subplot(121)
plt.hist(p_dane)
plt.title("Poisson")

plt.subplot(122)
plt.hist(g_dane)
plt.title("Gauss")

plt.show()