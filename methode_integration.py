import numpy as np
from scipy.integrate import trapezoid, simpson

def fonction_integrante(p: list, x):
    """
    Évalue le polynôme de degré 3 défini par les coefficients de la liste p au(x) point(s) x.
    Note : Bien que le commentaire initial mentionne un degré 4, la fonction s'arrête à x³.
    p = [p0, p1, p2, p3] -> p0 + p1*x + p2*x² + p3*x³
    """
    return p[0] + p[1] * x + p[2] * x ** 2 + p[3] * x ** 3


def integrale_exacte(p, a, b):
    """
    Calcule la valeur analytique (exacte) de l'intégrale en utilisant la primitive F(x).
    Applique le théorème fondamental de l'analyse : Intégrale = F(b) - F(a)
    """
    # Définition de la primitive F(x) obtenue par intégration terme à terme
    F = lambda x: (p[0] * x
                   + (p[1] * x ** 2) / 2
                   + (p[2] * x ** 3) / 3
                   + (p[3] * x ** 4) / 4)

    return F(b) - F(a)


# =============================================================================
# --- MÉTHODE DES RECTANGLES À GAUCHE (Ordre 1) ---
# =============================================================================

def methode_rectangle_classique(p, a, b, n):
    """
    Approximation de l'intégrale par la méthode des rectangles à gauche.
    Version standard utilisant une boucle 'for' (itérative).
    """
    dx = (b - a) / n  # Largeur de chaque sous-intervalle (pas de discrétisation)
    somme_aires = 0
    
    # Boucle sur chaque segment pour accumuler l'aire du rectangle associé
    for i in range(0, n):
        x_i = a + dx * i  # Évaluation au bord gauche du segment courant
        somme_aires += fonction_integrante(p, x_i) * dx
        
    return somme_aires


def methode_rectangle_numpy(p, a, b, n):
    """
    Approximation de l'intégrale par la méthode des rectangles à gauche.
    Version vectorisée utilisant NumPy pour éliminer la boucle Python.
    """
    dx = (b - a) / n
    # Génération instantanée de tous les points d'évaluation (bords gauches)
    x_i = a + dx * np.arange(n)
    # Évaluation globale de la fonction et somme vectorisée
    somme_aires = np.sum(fonction_integrante(p, x_i) * dx)
    return somme_aires


# =============================================================================
# --- MÉTHODE DES TRAPÈZES (Ordre 2) ---
# =============================================================================

def methode_trapeze_classique(p, a, b, n):
    """
    Approximation par la méthode des trapèzes.
    Version standard calculant l'aire de chaque trapèze segment par segment.
    """
    dx = (b - a) / n
    somme_aires = 0
    
    for i in range(0, n):
        x_i = a + dx * i        # Bord gauche du segment
        x_j = a + dx * (i + 1)  # Bord droit du segment
        # Aire du trapèze : (hauteur_gauche + hauteur_droite) * largeur / 2
        somme_aires += (fonction_integrante(p, x_i) + fonction_integrante(p, x_j)) * dx / 2
        
    return somme_aires


def methode_trapeze_numpy(p, a, b, n):
    """
    Approximation par la méthode des trapèzes.
    Version vectorisée appliquant la formule globale composite.
    """
    dx = (b - a) / n
    # Création du maillage contenant les n+1 points (du départ 'a' jusqu'à la fin 'b')
    x = a + dx * np.arange(n + 1)
    f_x = fonction_integrante(p, x)

    # Formule composite : les points aux extrémités (a et b) comptent pour 1,
    # tandis que tous les points internes [1:-1] sont comptés 2 fois car partagés par deux trapèzes.
    somme_aires = (dx / 2) * (f_x[0] + 2 * np.sum(f_x[1:-1]) + f_x[-1])
    return somme_aires


# =============================================================================
# --- MÉTHODE DE SIMPSON (Ordre 4) ---
# =============================================================================

def methode_simpson_classique(p, a, b, n):
    """
    Approximation par la méthode de Simpson (intégration via des arcs de paraboles).
    Version itérative évaluant le bord gauche, le milieu et le bord droit de chaque segment.
    """
    dx = (b - a) / n
    somme_aires = 0

    for i in range(n):
        x_i = a + dx * i        # Bord gauche
        x_j = a + dx * (i + 1)  # Bord droit
        x_m = (x_i + x_j) / 2   # Point milieu du segment

        # Formule de Simpson sur un segment : (dx/6) * [f(x_i) + 4*f(x_m) + f(x_j)]
        somme_aires += (dx / 6) * (fonction_integrante(p, x_i) + 4 * fonction_integrante(p, x_m) + fonction_integrante(p, x_j))
        
    return somme_aires


def methode_simpson_numpy(p, a, b, n):
    """
    Approximation par la méthode de Simpson.
    Version vectorisée séparant le traitement des bords de segments et des milieux.
    """
    dx = (b - a) / n
    
    # 1. Traitement des extrémités des n segments (les n+1 bornes)
    x_bords = a + dx * np.arange(n + 1)
    f_bords = fonction_integrante(p, x_bords)
    # Formule composite pour les bords (les points internes comptent double)
    somme_bords = f_bords[0] + 2 * np.sum(f_bords[1:-1]) + f_bords[-1]
    
    # 2. Traitement des milieux des n segments (les points à décalage +0.5)
    x_m = a + dx * (np.arange(n) + 0.5)
    f_m = fonction_integrante(p, x_m)
    s_m = 4 * np.sum(f_m)  # Les points milieux sont affectés du coefficient 4
    
    # Recomposition finale
    somme_aires = (dx / 6) * (somme_bords + s_m)
    return somme_aires


# =============================================================================
# --- MÉTHODES INTÉGRÉES (SCIPI) ---
# =============================================================================

def methode_trapeze_integree(p, a, b, n):
    """
    Utilise la fonction de bibliothèque native 'trapezoid' de SciPy.
    Idéal pour l'intégration de données discrètes pré-calculées.
    """
    # Génération d'une grille uniforme de 'n' points (ce qui crée n-1 intervalles)
    x = np.linspace(a, b, n) 
    y = fonction_integrante(p, x)
    return trapezoid(y, x=x) 


def methode_simpson_integree(p, a, b, n):
    """
    Utilise la fonction de bibliothèque native 'simpson' de SciPy.
    Remarque : Pour de meilleures performances et une précision optimale,
    il est recommandé que le nombre de points 'n' soit impair (nombre pair d'intervalles).
    """
    x = np.linspace(a, b, n) 
    y = fonction_integrante(p, x)
    return simpson(y, x=x)
