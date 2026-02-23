import math


def GenU(n, seed=42):
    x = seed
    a= 16897
    b= 0
    c= 2147483657
    liczby = []
    for _ in range(n):
        x = (a * x + b)%c
        liczby.append(x/c)

    return liczby

print(GenU(8))

def Poisson(lam):
    X = -1
    S = 1
    q = math.exp(-lam)
