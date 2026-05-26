import numpy as np


def fonction_integrante(p: list, x):
    return p[0] + p[1] * x + p[2] * x ** 2 + p[3] * x ** 3


def integrale_exacte(p, a, b):
    # Définition de la primitive F(x)
    F = lambda x: p[0] * x + (p[1] * x ** 2) / 2 + (p[2] * x ** 3) / 3 + (p[3] * x ** 4) / 4
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
