import numpy as np


def fonction_integrante(p: list, x):
    # p = [p0, p1, p2, p3, p4] -> p0 + p1*x + p2*x² + p3*x³ + p4*x⁴
    return p[0] + p[1] * x + p[2] * x ** 2 + p[3] * x ** 3 + p[4] * x ** 4


def integrale_exacte(p, a, b):
    # Définition de la primitive F(x) avec le terme de degré 4 intégré en x⁵/5
    F = lambda x: (p[0] * x
                   + (p[1] * x ** 2) / 2
                   + (p[2] * x ** 3) / 3
                   + (p[3] * x ** 4) / 4
                   + (p[4] * x ** 5) / 5)
    return F(b) - F(a)



# --- VRAIE MÉTHODE DES RECTANGLES (À gauche, ordre 1) ---
# À utiliser si vous voulez observer une erreur plus grande et une pente plus douce.

def methode_rectangle_classique(p, a, b, n):
    dx = (b - a) / n
    somme_aires = 0
    for i in range(0, n):
        x_i = a + dx * i  # Évaluation au bord gauche du segment
        somme_aires += fonction_integrante(p, x_i) * dx
    return somme_aires


def methode_rectangle_numpy(p, a, b, n):
    dx = (b - a) / n
    x_i = a + dx * np.arange(n)
    somme_aires = np.sum(fonction_integrante(p, x_i) * dx)
    return somme_aires


# --- MÉTHODE DES TRAPÈZES (Ordre 2) ---

def methode_trapeze_classique(p, a, b, n):
    dx = (b - a) / n
    somme_aires = 0
    for i in range(0, n):
        x_i = a + dx * i
        x_j = a + dx * (i + 1)
        somme_aires += (fonction_integrante(p, x_i) + fonction_integrante(p, x_j)) * dx / 2
    return somme_aires


def methode_trapeze_numpy(p, a, b, n):
    dx = (b - a) / n
    x = a + dx * np.arange(n + 1)
    f_x = fonction_integrante(p, x)

    # CORRECTION : Le slicing [1:-1] sélectionne exactement tous les points internes.
    # f_x[0] est le premier point, f_x[-1] est le dernier point (équivalent à f_x[n]).
    somme_aires = (dx / 2) * (f_x[0] + 2 * np.sum(f_x[1:-1]) + f_x[-1])
    return somme_aires

def methode_simpson_classique(p,a,b,n):
    dx = (b-a)/n
    somme_aires = 0

    for i in range(n):
        x_i = a+dx*i
        x_j = a+dx*(i+1)
        x_m = (x_i+x_j)/2

        somme_aires += (dx/6)*(fonction_integrante(p,x_i)+4*fonction_integrante(p,x_m)+fonction_integrante(p,x_j))
    return somme_aires

def methode_simpson_numpy(p,a,b,n):
    dx = (b-a)/n
    x_bords = a+dx*np.arange(n+1)
    f_bords = fonction_integrante(p,x_bords)
    somme_bords = f_bords[0]+2*np.sum(f_bords[1:-1])+f_bords[-1]
    x_m = a+dx*(np.arange(n)+0.5)
    f_m = fonction_integrante(p,x_m)
    s_m = 4*np.sum(f_m)
    somme_aires = (dx/6)*(somme_bords+s_m)
    return somme_aires


