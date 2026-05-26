import numpy as np

def fonction_integrante(p:list,x):
    return p[0]+p[1]*x+p[2]*x**2+p[3]*x**3


def integrale_exacte(p, a, b):
    # Définition de la primitive F(x) sous forme de lambda
    F = lambda x: p[0] * x + (p[1] * x ** 2) / 2 + (p[2] * x ** 3) / 3 + (p[3] * x ** 4) / 4
    return F(b) - F(a)


def methode_rectangle_classique(p,a,b,n):
    dx = (b-a)/n
    somme_aires = 0
    for i in range(0,n):
        x_i = a+dx*(i+0.5)
        somme_aires += fonction_integrante(p,x_i)*dx
    return somme_aires

def methode_rectangle_numpy(p, a, b, n):
    dx = (b - a) / n
    x_i = a + dx * (np.arange(n) + 0.5)
    somme_aires = np.sum(fonction_integrante(p, x_i) * dx)
    return somme_aires
