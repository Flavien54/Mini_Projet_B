"""
methode_integration.py
======================
Module regroupant toutes les fonctions d'intégration numérique utilisées dans le
Mini-Projet B (MGA 802).
 
Méthodes implémentées :
    - Rectangle (Python et NumPy)
    - Trapèze   (Python et NumPy)
    - Simpson   (Python et NumPy)
    - Trapèze intégré  (scipy.integrate.trapezoid)
    - Simpson intégré  (scipy.integrate.simpson)
 
Chaque méthode est disponible en deux versions :
    - « classique » : boucle Python pure, plus lisible mais plus lente.
    - « numpy »     : vectorisée avec NumPy, beaucoup plus rapide pour grand n.
"""

import numpy as np
from scipy.integrate import trapezoid, simpson

# ==============================================================================
# FONCTION À INTÉGRER
# ==============================================================================

def fonction_integrante(p: list, x):    # p = [p0, p1, p2, p3, p4] -> p0 + p1*x + p2*x² + p3*x³ + p4*x⁴
     """
    Évalue le polynôme du 3e ordre f(x) = p0 + p1·x + p2·x² + p3·x³.
 
    Paramètres
    ----------
    p : list de 4 coefficients [p0, p1, p2, p3]
    x : float ou tableau NumPy — point(s) où évaluer f
 
    Retour
    ------
    Valeur(s) de de f(x), de même type que x.
    """
    return p[0] + p[1] * x + p[2] * x ** 2 + p[3] * x ** 3

# ==============================================================================
# SOLUTION ANALYTIQUE EXACTE
# ==============================================================================

def integrale_exacte(p, a, b):
    # Définition de la primitive F(x) avec le terme de degré 4 intégré en x⁵/5
    """
    Calcule la valeur exacte de ∫_a^b f(x) dx par intégration analytique.
 
    La primitive de f(x) = p0 + p1·x + p2·x² + p3·x³ est :
        F(x) = p0·x + p1·x²/2 + p2·x³/3 + p3·x⁴/4
 
    On applique le théorème fondamental : I_exact = F(b) - F(a).
    Cette valeur sert de référence pour mesurer l'erreur des méthodes numériques.
 
    Paramètres
    ----------
    p : list — coefficients du polynôme
    a, b : float — bornes d'intégration
 
    Retour
    ------
    float — valeur exacte de l'intégrale.
    """
    # Primitive F(x) évaluée en un point x
    F = lambda x: (p[0] * x
                   + (p[1] * x ** 2) / 2
                   + (p[2] * x ** 3) / 3
                   + (p[3] * x ** 4) / 4)

    return F(b) - F(a)



# ==============================================================================
# MÉTHODE DES RECTANGLES  (ordre de convergence : O(h¹))
# ==============================================================================
# Principe : on divise [a, b] en n segments de largeur h = (b-a)/n.
# Sur chaque segment, f est approchée par sa valeur au bord GAUCHE.
# L'aire du rectangle i vaut f(x_i) · h.
# Erreur globale proportionnelle à h  →  convergence en O(n⁻¹).
# ==============================================================================

def methode_rectangle_classique(p, a, b, n):
     """
    Intégration par la méthode des rectangles (bord gauche) — Python pur.
 
    Boucle explicite sur les n segments : lisible mais lente pour grand n
    car chaque itération est interprétée par Python.
 
    Paramètres
    ----------
    p    : list  — coefficients du polynôme
    a, b : float — bornes d'intégration
    n    : int   — nombre de segments
 
    Retour
    ------
    float — valeur approchée de l'intégrale.
    """
    dx = (b - a) / n # Largeur uniforme de chaque segment
    somme_aires = 0

    for i in range(0, n):
        x_i = a + dx * i  # Abscisse du bord gauche du segment i
        somme_aires += fonction_integrante(p, x_i) * dx # Aire du rectangle i
    return somme_aires


def methode_rectangle_numpy(p, a, b, n):
     """
    Intégration par la méthode des rectangles (bord gauche) — version NumPy.
 
    Toutes les abscisses sont calculées en une seule opération vectorielle,
    ce qui évite la boucle Python et exploite les routines C optimisées de NumPy.
 
    Paramètres
    ----------
    p    : list  — coefficients du polynôme
    a, b : float — bornes d'intégration
    n    : int   — nombre de segments
 
    Retour
    ------
    float — valeur approchée de l'intégrale.
    """
    dx = (b - a) / n

    # Vecteur des n abscisses gauches : [a, a+dx, a+2·dx, ..., a+(n-1)·dx]
    x_i = a + dx * np.arange(n)

    # Évaluation vectorielle de f puis somme pondérée par dx
    somme_aires = np.sum(fonction_integrante(p, x_i) * dx)
    return somme_aires


# ==============================================================================
# MÉTHODE DES TRAPÈZES  (ordre de convergence : O(h²))
# ==============================================================================
# Principe : sur chaque segment [x_i, x_{i+1}], on remplace f par la droite
# passant par (x_i, f(x_i)) et (x_{i+1}, f(x_{i+1})).
# L'aire du trapèze i vaut (f(x_i) + f(x_{i+1})) · h / 2.
# La formule composite peut se réécrire :
#   I ≈ h/2 · [f(x_0) + 2·f(x_1) + 2·f(x_2) + ... + 2·f(x_{n-1}) + f(x_n)]
# Erreur globale en O(h²)  →  convergence en O(n⁻²), plus rapide qu'au rectangle.
# ==============================================================================

def methode_trapeze_classique(p, a, b, n):
    """
    Intégration par la méthode des trapèzes — Python pur.
 
    Pour chaque segment, la moyenne des valeurs de f aux deux extrémités
    est multipliée par la largeur h pour obtenir l'aire du trapèze.
 
    Paramètres
    ----------
    p    : list  — coefficients du polynôme
    a, b : float — bornes d'intégration
    n    : int   — nombre de segments
 
    Retour
    ------
    float — valeur approchée de l'intégrale.
    """
    dx = (b - a) / n
    somme_aires = 0
    for i in range(0, n):
        x_i = a + dx * i         # Borne gauche du segment i
        x_j = a + dx * (i + 1)   # Borne droite du segment i
        
        # Aire du trapèze : moyenne des deux valeurs × largeur
        somme_aires += (fonction_integrante(p, x_i) + fonction_integrante(p, x_j)) * dx / 2
    return somme_aires


def methode_trapeze_numpy(p, a, b, n):
    """
    Intégration par la méthode des trapèzes — version NumPy.
 
    Utilise la formule composite réécrite avec pondérations :
        I ≈ (h/2) · [f_0 + 2·(f_1 + f_2 + ... + f_{n-1}) + f_n]
 
    Le slicing f_x[1:-1] sélectionne tous les points INTÉRIEURS (ni le premier
    ni le dernier), auxquels on applique le coefficient 2.
 
    Paramètres
    ----------
    p    : list  — coefficients du polynôme
    a, b : float — bornes d'intégration
    n    : int   — nombre de segments
 
    Retour
    ------
    float — valeur approchée de l'intégrale.
    """
    dx = (b - a) / n

    # n+1 points équidistants : x_0 = a, x_1, ..., x_n = b
    x = a + dx * np.arange(n + 1)
    f_x = fonction_integrante(p, x)

    # CORRECTION : Le slicing [1:-1] sélectionne exactement tous les points internes.
    # f_x[0] est le premier point, f_x[-1] est le dernier point (équivalent à f_x[n]).
    somme_aires = (dx / 2) * (f_x[0] + 2 * np.sum(f_x[1:-1]) + f_x[-1])
    return somme_aires


# ==============================================================================
# MÉTHODE DE SIMPSON  (ordre de convergence : O(h⁴))
# ==============================================================================
# Principe : sur chaque segment [x_i, x_{i+1}], f est approchée par une parabole
# passant par les deux extrémités et le milieu m = (x_i + x_{i+1}) / 2.
# Formule de Simpson sur un segment :
#   I_i ≈ (h/6) · [f(x_i) + 4·f(m) + f(x_{i+1})]
# Erreur globale en O(h⁴)  →  convergence très rapide (O(n⁻⁴)).
# Note : pour un polynôme de degré ≤ 3, Simpson est EXACTE (erreur = précision machine).
# ==============================================================================
def methode_simpson_classique(p,a,b,n):
    """
    Intégration par la méthode de Simpson — Python pur.
 
    Pour chaque segment, on évalue f en trois points : les deux bords et le milieu.
    La pondération (1, 4, 1) × h/6 provient de l'intégration exacte d'une parabole.
 
    Paramètres
    ----------
    p    : list  — coefficients du polynôme
    a, b : float — bornes d'intégration
    n    : int   — nombre de segments
 
    Retour
    ------
    float — valeur approchée de l'intégrale (exacte pour polynômes de degré ≤ 3).
    """
    dx = (b-a)/n
    somme_aires = 0

    for i in range(n):
        x_i = a+dx*i        # Borne gauche
        x_j = a+dx*(i+1)    # Borne droite
        x_m = (x_i+x_j)/2   # Point milieu du segment

        # Formule de Simpson : pondérations 1, 4, 1 sur les trois points
        somme_aires += (dx/6)*(fonction_integrante(p,x_i)+4*fonction_integrante(p,x_m)+fonction_integrante(p,x_j))
    return somme_aires

def methode_simpson_numpy(p,a,b,n):
    """
    Intégration par la méthode de Simpson — version NumPy.
 
    On sépare les contributions en deux groupes vectorisés :
      1. Points aux BORDS des segments (pondération 1 pour les extrémités globales,
         2 pour les bords partagés entre deux segments adjacents).
      2. Points MILIEUX de chaque segment (pondération 4).
 
    Paramètres
    ----------
    p    : list  — coefficients du polynôme
    a, b : float — bornes d'intégration
    n    : int   — nombre de segments
 
    Retour
    ------
    float — valeur approchée de l'intégrale.
    """
    
    dx = (b-a)/n

    # --- Contribution des bords (n+1 points) ---
    x_bords = a+dx*np.arange(n+1)
    f_bords = fonction_integrante(p,x_bords)
    # Pondérations : 1 pour les deux extrémités, 2 pour tous les points intérieurs
    somme_bords = f_bords[0]+2*np.sum(f_bords[1:-1])+f_bords[-1]

      # --- Contribution des milieux (n points) ---
    x_m = a+dx*(np.arange(n)+0.5)      # Centre de chaque segment
    f_m = fonction_integrante(p,x_m)
    s_m = 4*np.sum(f_m)                # Pondération 4 pour chaque milieu
    
    # Somme globale pondérée par h/6
    somme_aires = (dx/6)*(somme_bords+s_m)
    return somme_aires

# ==============================================================================
# MÉTHODES PRÉ-PROGRAMMÉES (scipy.integrate)
# ==============================================================================
# SciPy fournit des implémentations optimisées de la règle du trapèze et de
# Simpson. On les utilise ici comme référence pour valider nos propres versions
# et comparer les temps d'exécution.
# ==============================================================================
def methode_trapeze_integree(p, a, b,n):
     """
    Intégration par la méthode des trapèzes via scipy.integrate.trapezoid.
 
    On génère n points équidistants avec np.linspace, on évalue f sur ces
    points, puis on délègue le calcul à la fonction SciPy.
 
    Paramètres
    ----------
    p    : list  — coefficients du polynôme
    a, b : float — bornes d'intégration
    n    : int   — nombre de points (= nombre de segments + 1)
 
    Retour
    ------
    float — valeur approchée de l'intégrale.
    """
    x = np.linspace(a, b, n) # 101 points pour avoir 100 intervalles
    y = fonction_integrante(p, x)
    return trapezoid(y, x=x) # On spécifie x=x ici : cipy calcule la règle composite des trapèzes

def methode_simpson_integree(p, a, b, n):
    """
    Intégration par la méthode de Simpson via scipy.integrate.simpson.
 
    Un nombre IMPAIR de points (n pair de segments) est idéal pour que SciPy
    puisse appliquer la règle de Simpson composite sans avoir recours à des
    formules de correction en bout d'intervalle.
 
    Paramètres
    ----------
    p    : list  — coefficients du polynôme
    a, b : float — bornes d'intégration
    n    : int   — nombre de points (idéalement impair)
 
    Retour
    ------
    float — valeur approchée de l'intégrale.
    """
    x = np.linspace(a, b, n) # Nombre impair de points idéal pour Simpson (n points équidistants sur [a, b])
    y = fonction_integrante(p, x)
    return simpson(y, x=x) # On spécifie x=x ici




