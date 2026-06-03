# MGA802 — Mini-Projet B : Analyse Numérique
**École de Technologie Supérieure - Programmation Python (MGA802) - Été 2026**

Équipe : BLANCHARD Flavien · MECHREF Milissa · CONDETTE Vincent


## Table des matières

- [Aperçu du projet](#aperçu-du-projet)
- [Méthodes d'intégration étudiées](#méthodes-dintégration-étudiées)
- [Structure du projet](#structure-du-projet)
- [Choix de conception](#choix-de-conception)
- [Installation et Prérequis](#installation-et-prérequis)
- [Instructions d'exécution](#instructions-dexécution)
- [Performances et Analyse](#performances-et-analyse)
- [Résultats et livrables](#résultats-et-livrables)

---

## Aperçu du projet

L'objectif principal est de démontrer la performance de la bibliothèque NumPy pour le calcul numérique, en le comparant avec des méthodes Python de base. 

Ce programme calcule l'aire sous la courbe d'une fonction polynomiale du 3e ordre, de la forme : `f(x) = p0 + p1*x + p2*x^2 + p3*x^3`. Pour évaluer la précision des méthodes numériques, une solution analytique exacte est calculée et sert de  référence pour déterminer l'erreur d'approximation.

---

## Méthodes d'intégration étudiées

Le programme compare différentes approches et évalue la convergence et la vitesse d'exécution pour chacune d'elles. Pour chaque algorithme, on trouve une version en Python "classique" et une version avec NumPy :

* **Méthode des rectangles :** Divise l'intervalle d'intégration en segments réguliers et évalue la fonction au bord gauche de chaque segment. Méthode d'ordre 1.
* **Méthode des trapèzes :** Approxime l'aire sous la courbe en utilisant des trapèzes sur chaque segment. Méthode d'ordre 2.
* **Méthode de Simpson :** Combine la méthode des trapèzes et des paraboles pour obtenir une approximation bien plus précise de l'intégrale.
* **Méthodes pré-programmées :** Comparaison avec les fonctions natives de  `scipy.integrate` (`trapezoid` et `simpson`) qui sert de référence pour valider les implémentations et mesurer l'écart de performance.

---

## Structure du projet

```text

├── analyse_numerique.py     
# main : exécute les boucles, évalue le temps des méthodes, vérifie et trace les graphiques
├── methode_integration.py   
# Module contenant les 8 algorithmes d'intégration et le calcul d'erreur
├── rapport.pdf              
# Rapport d'analyse numérique (interprétation des graphiques)
```

**Note :** Le script importe `methode_integration.py` qui regroupe toutes les opérations mathématiques utilisées dans `analyse_numerique.py`.

---

## Choix de conception

Afin de garantir la fiabilité de nos analyses numériques, plusieurs choix ont été pris :

- Séparation de la logique mathématique avec le fichier (`methode_integration.py`) par rapport au script principal pour l'affichage (`analyse_numerique.py`).

- Haute précision : Utilisation exclusive de time.perf_counter() pour chronométrer les temps d'exécution. Cette fonction mesure avec précision les opérations quasi-instantanées de NumPy, alors qu'un simple time.time() serait insuffisant.
---

## Installation et Prérequis

**Prérequis :** Python 3.8 ou supérieur.


```bash
# 1. Cloner le dépôt
git clone <url-du-depot>
cd mga802-miniprojetb

# 2. Installer les bibliothèques scientifiques requises
pip install numpy scipy matplotlib

```


## Instructions d'exécution

L'execution du script principal suffit pour lancer l'intégralité des calculs, des chronométrages et la génération des graphiques. Ce programme ne nécessite pas de CLI complexe.

**Ce que fait le script :**
1. Définit les paramètres du polynôme `p = [7, 23, 3e4, 51]` sur l'intervalle `[0, 1]`.
2. Calcule la solution analytique exacte.
3. Teste itérativement chaque méthode pour un nombre `n` de segments allant de 10 à 10 000.
4. Chronomètre (`time.perf_counter`) et valide les écarts de résultats mathématiques entre les approches.
5. Génère, sauvegarde, puis affiche les graphiques Matplotlib qui renvoient le comportement des algorithmes.

---

## Performances et Analyse

| Méthode | Ordre de convergence | Temps d'exécution (Python de base) | Temps d'exécution (NumPy) |
|---|---|---|---|
| **Rectangles** | $O(h^{{1}})$ | Lent (boucle `for`) | **Très rapide** (Vectorisation) |
| **Trapèzes** | $O(h^{{2}})$ | Lent (boucle `for`) | **Très rapide** (Vectorisation) |
| **Simpson** | $O(h^{{4}})$ | Lent (boucle `for`) | **Très rapide** (Vectorisation) |

* **Vérification (`assert`) :** Le code intègre des tests automatiques à l'exécution s'assurant que les résultats classiques et vectorisés (NumPy) sont mathématiquement équivalents à `1e-10` près.

---

## Résultats et livrables

- Ce `README.md` mis à jour avec :
  - Description du programme
  - Instructions d'installation et d'exécution
  - Auteurs (membres de l'équipe)
  - Choix de conception (utilisation de `time.perf_counter`...)

- `comparaison_methodes_integration.pdf` : Une figure complète contenant 3 sous-graphiques :
   - Convergence des erreurs (échelle logarithmique).
   - Temps d'exécution de toutes les méthodes selon $n$.
   - Diagramme à barres comparatif de l'erreur absolue sur des échantillons choisis ($n=10, 50, \dots$).
- `zoom_convergence_simpson.pdf` : Un zoom analytique mettant en évidence la pente théorique en $O(n^{{-4}})$ de la méthode de Simpson et la saturation due à la précision de la machine.
"""
- Un **rapport pdf de 4 pages max** couvrant les aspects d'analyses numériques, incluant l'interprétation des résultats obtenus, des graphiques de convergence, du temps de calcul et des erreurs.
