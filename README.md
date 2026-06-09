# MGA802 — Mini-Projet B : Analyse Numérique
**École de Technologie Supérieure — Programmation Python (MGA802) — Été 2026**

Équipe : BLANCHARD Flavien · MECHREF Milissa · CONDETTE Vincent

---

## Table des matières

- [Aperçu du projet](#aperçu-du-projet)
- [Méthodes d'intégration étudiées](#méthodes-dintégration-étudiées)
- [Structure du projet](#structure-du-projet)
- [Choix de conception](#choix-de-conception)
- [Installation et prérequis](#installation-et-prérequis)
- [Instructions d'exécution](#instructions-dexécution)
- [Performances et analyse](#performances-et-analyse)
- [Résultats et livrables](#résultats-et-livrables)

---

## Aperçu du projet

L'objectif de ce mini-projet est de **démontrer le gain de performance de NumPy** pour le calcul numérique, en le comparant à des implémentations Python pures (boucles `for`).

Le programme calcule l'intégrale définie d'un polynôme de degré 3 de la forme :

$$f(x) = p_0 + p_1 x + p_2 x^2 + p_3 x^3$$

Une **solution analytique exacte** (calculée via la primitive) sert de référence pour quantifier l'erreur d'approximation de chaque méthode numérique, en fonction du nombre de segments $n$.

---

## Méthodes d'intégration étudiées

Pour chaque algorithme, deux versions sont implémentées et comparées :

| Méthode | Description | Ordre de convergence |
|---|---|---|
| **Rectangles (gauche)** | Évalue $f$ au bord gauche de chaque segment | $O(h^1)$ |
| **Trapèzes** | Approche linéaire entre les deux bornes de chaque segment | $O(h^2)$ |
| **Simpson** | Ajustement parabolique sur chaque segment (bord gauche, milieu, bord droit) | $O(h^4)$ |
| **SciPy (référence)** | `scipy.integrate.trapezoid` et `simpson` pour validation | — |

> **Note sur Simpson :** La méthode de Simpson est exacte pour tout polynôme de degré ≤ 3, ce qui implique une saturation rapide à l'erreur machine (≈ `1e-15`) pour le polynôme étudié ici.

---

## Structure du projet

```text
mga802-miniprojetb/
├── analyse_numerique.py      # Script principal : boucles de tests, chronométrage, génération des figures
├── methode_integration.py    # Module mathématique : 8 algorithmes d'intégration + solution exacte
├── rapport.pdf               # Rapport d'analyse numérique (4 pages max)
└── README.md                 # Ce fichier
```

**Séparation des responsabilités :**
- `methode_integration.py` : contient exclusivement la logique mathématique (fonctions pures, sans effet de bord).
- `analyse_numerique.py` : orchestre les appels, mesure les temps, valide les résultats (`assert`) et produit les figures Matplotlib.

---

## Choix de conception

### Chronométrage avec `time.perf_counter()`

Les opérations NumPy vectorisées sont quasi-instantanées (de l'ordre de la microseconde). `time.time()` a une résolution trop faible pour les capturer fidèlement. `time.perf_counter()` offre la **plus haute résolution disponible** sur le système et est la référence recommandée pour le benchmarking de code Python.

### Vectorisation NumPy vs. boucles Python

Chaque algorithme existe en deux versions :

- **Version classique** (`for`) : lisible, pédagogique, mais coûteuse car chaque itération interprète du bytecode Python.
- **Version NumPy** : élimine les boucles en traitant les tableaux entiers en un seul appel C. Les gains typiques observés sont d'**un à deux ordres de grandeur**.

### Vérification automatique (`assert`)

Des assertions à `1e-10` près garantissent que les deux versions (classique et NumPy) de chaque méthode produisent des résultats **mathématiquement équivalents** avant de procéder aux mesures de performance.

### Paramètres du cas test

Le polynôme utilisé est `p = [7, 23, 3e4, 51]` sur l'intervalle `[0, 1]`. Le coefficient `p2 = 3e4` est volontairement large pour accentuer la courbure et rendre les erreurs d'approximation plus visibles aux faibles valeurs de $n$.

---

## Installation et prérequis

**Prérequis :** Python 3.8 ou supérieur.

```bash
# 1. Cloner le dépôt
git clone <url-du-depot>
cd mga802-miniprojetb

# 2. Installer les dépendances
pip install numpy scipy matplotlib
```

**Dépendances utilisées :**

| Bibliothèque | Usage |
|---|---|
| `numpy` | Vectorisation des calculs numériques |
| `scipy` | Fonctions de référence `trapezoid` et `simpson` |
| `matplotlib` | Génération et export des figures |

---

## Instructions d'exécution

```bash
python analyse_numerique.py
```

Aucun argument en ligne de commande n'est nécessaire. Le script exécute automatiquement les étapes suivantes :

1. Définit le polynôme `p = [7, 23, 3e4, 51]` sur `[0, 1]`.
2. Calcule la valeur exacte de référence via la primitive analytique.
3. Pour $n \in [10, 10\,000]$, évalue chaque méthode, chronomètre son exécution et calcule l'erreur absolue.
4. Vérifie par `assert` la cohérence entre versions classique et NumPy (tolérance `1e-10`).
5. Génère, sauvegarde et affiche les figures décrites dans la section [Résultats](#résultats-et-livrables).

---

## Performances et analyse

### Convergence théorique

| Méthode | Erreur en $O(…)$ | Comportement attendu |
|---|---|---|
| Rectangles | $O(h^1) = O(n^{-1})$ | Pente −1 sur graphe log-log |
| Trapèzes | $O(h^2) = O(n^{-2})$ | Pente −2 sur graphe log-log |
| Simpson | $O(h^4) = O(n^{-4})$ | Pente −4, puis plateau à ≈ `1e-15` |

### Performance d'exécution

| Méthode | Python classique | NumPy vectorisé |
|---|---|---|
| Rectangles | Lent (`for` sur $n$ itérations) | Très rapide (1 appel vectoriel) |
| Trapèzes | Lent | Très rapide |
| Simpson | Lent | Très rapide |

> Pour $n = 10\,000$, le gain typique de NumPy est d'environ **×100 à ×1000** selon la machine.

---

## Résultats et livrables

### Figures générées automatiquement

**`comparaison_methodes_integration.pdf`** — Figure principale en 3 sous-graphiques :
- Convergence des erreurs absolues en échelle logarithmique (log-log), avec les pentes théoriques tracées en référence.
- Temps d'exécution de toutes les méthodes en fonction de $n$.
- Diagramme à barres comparatif de l'erreur absolue pour $n \in \{10, 50, \ldots\}$.

**`zoom_convergence_simpson.pdf`** — Zoom analytique mettant en évidence :
- La pente théorique en $O(n^{-4})$ de la méthode de Simpson.
- La saturation numérique due à la précision machine (≈ `1e-15`).

### Rapport

`rapport.pdf` — Rapport de 4 pages maximum couvrant :
- Interprétation des graphiques de convergence et de temps de calcul.
- Analyse comparative des erreurs absolues par méthode.
- Discussion sur les limites de précision (erreur machine, saturation de Simpson).

---

*MGA802 — École de Technologie Supérieure, Montréal — Été 2026*
