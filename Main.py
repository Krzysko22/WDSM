import math
import numpy as np

S = 10      #liczba kanałów
Lambda = 1  #Natężenie ruchu
N = 60      #Średnia długość rozmowy
sigma = 5   #Odchylenie standardowe
min = 10    #Minimalna długość rozmowy
maks= 60    #Maksymalna długość rozmowy
kolejka= 5  #Długość kolejki
sym= 100    #Czas symulacji

#Generatory Poissona i Gaussa
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
        if U == 0: continue
        X = V / U
        if X**2 <= -4 * math.log(U):
            return mu + X * sigma
#------------

#Generowanie listy
lista_polaczen = []
obecnyczas = 0  #Obecny czas przyjścia
while obecnyczas > sym:
    nastepne_przybycie = np.random.poisson(Lambda)
    obecnyczas +=1

    for _ in range (nastepne_przybycie):
        dlugosc = Gauss(N,sigma)
        dlugosc = max(min,min(maks,dlugosc))
        lista_polaczen.append(obecnyczas, int(dlugosc), int(dlugosc))

#Symulacja krokowa



