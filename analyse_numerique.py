import numpy as np
import matplotlib.pyplot as plt
import methode_integration
import time


def main():

    # ==========================================================
    # PARAMÈTRES DE LA SIMULATION
    # ==========================================================

    # Coefficients du polynôme ou paramètres passés à la fonction à intégrer
    p = [1e10, 2e-10, 3e-18, 4e5]
    
    # Bornes d'intégration [a, b]
    a, b = 0, 1

    # Calcul de la valeur de référence (analytique) pour évaluer l'erreur globale
    exact_integral = methode_integration.integrale_exacte(p, a, b)

    # Liste des nombres de sous-intervalles (segments) testés pour analyser la convergence
    n_values = np.array([10, 20, 50, 100, 200, 500, 1000, 2000, 4000, 10000])

    # ==========================================================
    # STRUCTURES DE STOCKAGE DES RÉSULTATS
    # ==========================================================

    # Listes pour stocker l'erreur absolue de chaque méthode
    errors_rectangle_classique, errors_rectangle_numpy = [], []
    errors_trapeze_classique, errors_trapeze_numpy = [], []
    errors_simpson_classique, errors_simpson_numpy = [], []
    errors_simpson_integree, errors_trapeze_integree = [], []

    # Listes pour stocker le temps d'exécution (en secondes) de chaque méthode
    times_rectangle_classique, times_rectangle_numpy = [], []
    times_trapeze_classique, times_trapeze_numpy = [], []
    times_simpson_classique, times_simpson_numpy = [], []
    times_simpson_integree, times_trapeze_integree = [], []

    # ==========================================================
    # BOUCLE DE CALCUL ET DE BENCHMARK
    # ==========================================================

    for n in n_values:

        # --- Méthode des Rectangles (Boucle classique) ---
        t0 = time.perf_counter()
        rect_class = methode_integration.methode_rectangle_classique(p, a, b, n)
        t_rect_class = time.perf_counter() - t0

        # --- Méthode des Rectangles (Vectorisée avec NumPy) ---
        t0 = time.perf_counter()
        rect_np = methode_integration.methode_rectangle_numpy(p, a, b, n)
        t_rect_np = time.perf_counter() - t0

        # --- Méthode des Trapèzes (Boucle classique) ---
        t0 = time.perf_counter()
        trap_class = methode_integration.methode_trapeze_classique(p, a, b, n)
        t_trap_class = time.perf_counter() - t0

        # --- Méthode des Trapèzes (Vectorisée avec NumPy) ---
        t0 = time.perf_counter()
        trap_np = methode_integration.methode_trapeze_numpy(p, a, b, n)
        t_trap_np = time.perf_counter() - t0

        # --- Méthode de Simpson (Boucle classique) ---
        t0 = time.perf_counter()
        simp_class = methode_integration.methode_simpson_classique(p, a, b, n)
        t_simp_class = time.perf_counter() - t0

        # --- Méthode de Simpson (Vectorisée avec NumPy) ---
        t0 = time.perf_counter()
        simp_np = methode_integration.methode_simpson_numpy(p, a, b, n)
        t_simp_np = time.perf_counter() - t0

        # --- Méthode de Simpson Intégrée (via bibliothèques natives type SciPy ou fonction dédiée) ---
        t0 = time.perf_counter()
        simp_int = methode_integration.methode_simpson_integree(p, a, b, n + 1)
        t_simp_int = time.perf_counter() - t0

        # --- Méthode des Trapèzes Intégrée (via bibliothèques natives) ---
        t0 = time.perf_counter()
        trap_int = methode_integration.methode_trapeze_integree(p, a, b, n + 1)
        t_trap_int = time.perf_counter() - t0

        # --- Validations de cohérence ---
        # On s'assure que les versions classiques et vectorisées (NumPy) donnent bien le même résultat
        assert np.isclose(rect_class, rect_np, rtol=1e-10)
        assert np.isclose(trap_class, trap_np, rtol=1e-10)
        assert np.isclose(simp_class, simp_np, rtol=1e-10)

        # --- Calcul et stockage des erreurs absolues ---
        errors_rectangle_classique.append(abs(rect_class - exact_integral))
        errors_rectangle_numpy.append(abs(rect_np - exact_integral))

        errors_trapeze_classique.append(abs(trap_class - exact_integral))
        errors_trapeze_numpy.append(abs(trap_np - exact_integral))

        errors_simpson_classique.append(abs(simp_class - exact_integral))
        errors_simpson_numpy.append(abs(simp_np - exact_integral))

        errors_simpson_integree.append(abs(simp_int - exact_integral))
        errors_trapeze_integree.append(abs(trap_int - exact_integral))

        # --- Stockage des temps d'exécution ---
        times_rectangle_classique.append(t_rect_class)
        times_rectangle_numpy.append(t_rect_np)

        times_trapeze_classique.append(t_trap_class)
        times_trapeze_numpy.append(t_trap_np)

        times_simpson_classique.append(t_simp_class)
        times_simpson_numpy.append(t_simp_np)

        times_simpson_integree.append(t_simp_int)
        times_trapeze_integree.append(t_trap_int)

    # ==========================================================
    # CONFIGURATION DES GRAPHIQUES (STYLE)
    # ==========================================================

    plt.style.use('ggplot')  # Application du style visuel 'ggplot'

    # ==========================================================
    # FIGURE 1 : COMPARAISON GÉNÉRALE (CONVERGENCE, TEMPS & BARRES)
    # ==========================================================

    fig1 = plt.figure(figsize=(12, 14))

    # ----------------------------------------------------------
    # Sous-graphique 1 : Évolution de l'erreur (Échelle Log-Log)
    # ----------------------------------------------------------
    plt.subplot(3, 1, 1)

    # Courbes pour les méthodes des Rectangles
    plt.loglog(n_values, errors_rectangle_classique, 'b-', label='Rectangle Classique', linewidth=2)
    plt.loglog(n_values, errors_rectangle_numpy, 'r--', label='Rectangle NumPy', linewidth=2)

    # Courbes pour les méthodes des Trapèzes
    plt.loglog(n_values, errors_trapeze_classique, 'g-', label='Trapèze Classique', linewidth=2)
    plt.loglog(n_values, errors_trapeze_numpy, 'k--', label='Trapèze NumPy', linewidth=2)

    # Courbes pour les méthodes de Simpson
    plt.loglog(n_values, errors_simpson_classique, 'c-', label='Simpson Classique', linewidth=2)
    plt.loglog(n_values, errors_simpson_numpy, 'm--', label='Simpson NumPy', linewidth=2)

    # Courbes pour les variantes intégrées
    plt.loglog(n_values, errors_simpson_integree, color='darkred', linestyle='-', label='Simpson Intégrée', linewidth=2)
    plt.loglog(n_values, errors_trapeze_integree, color='orange', linestyle='--', label='Trapèze Intégrée', linewidth=2)

    plt.xlabel('Nombre de segments (n)')
    plt.ylabel('Erreur absolue')
    plt.title("Convergence des méthodes d'intégration")
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend()

    # ----------------------------------------------------------
    # Sous-graphique 2 : Évolution des temps de calcul (Échelle Log-Log)
    # ----------------------------------------------------------
    plt.subplot(3, 1, 2)

    # Affichage du coût temporel face à l'augmentation de la discrétisation (n)
    plt.loglog(n_values, times_rectangle_classique, 'b-', label='Rectangle Classique', linewidth=2)
    plt.loglog(n_values, times_rectangle_numpy, 'r--', label='Rectangle NumPy', linewidth=2)

    plt.loglog(n_values, times_trapeze_classique, 'g-', label='Trapèze Classique', linewidth=2)
    plt.loglog(n_values, times_trapeze_numpy, 'k--', label='Trapèze NumPy', linewidth=2)

    plt.loglog(n_values, times_simpson_classique, 'c-', label='Simpson Classique', linewidth=2)
    plt.loglog(n_values, times_simpson_numpy, 'm--', label='Simpson NumPy', linewidth=2)

    plt.loglog(n_values, times_simpson_integree, color='darkred', linestyle='-', label='Simpson Intégrée', linewidth=2)
    plt.loglog(n_values, times_trapeze_integree, color='orange', linestyle='--', label='Trapèze Intégrée', linewidth=2)

    plt.xlabel('Nombre de segments (n)')
    plt.ylabel('Temps de calcul (s)')
    plt.title("Performance des méthodes d'intégration")
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend()

    # ----------------------------------------------------------
    # Sous-graphique 3 : Histogrammes comparatifs des erreurs
    # ----------------------------------------------------------
    plt.subplot(3, 1, 3)

    # Sélection de quelques valeurs de n représentatives pour l'affichage en barres
    n_samples = [10, 50, 100, 500, 1000]
    indices = [np.where(n_values == n)[0][0] for n in n_samples] # Récupération des index correspondants

    x_pos = np.arange(len(indices))  # Position centrale de chaque groupe de barres
    width = 0.09                     # Largeur d'une barre individuelle

    # Génération juxtaposée des barres pour chaque méthode (décalage appliqué via la largeur)
    plt.bar(x_pos - 3.5 * width, [errors_rectangle_classique[i] for i in indices], width, label='Rectangle Classique')
    plt.bar(x_pos - 2.5 * width, [errors_rectangle_numpy[i] for i in indices], width, label='Rectangle NumPy')

    plt.bar(x_pos - 1.5 * width, [errors_trapeze_classique[i] for i in indices], width, label='Trapèze Classique')
    plt.bar(x_pos - 0.5 * width, [errors_trapeze_numpy[i] for i in indices], width, label='Trapèze NumPy')

    plt.bar(x_pos + 0.5 * width, [errors_simpson_classique[i] for i in indices], width, label='Simpson Classique')
    plt.bar(x_pos + 1.5 * width, [errors_simpson_numpy[i] for i in indices], width, label='Simpson NumPy')

    plt.bar(x_pos + 2.5 * width, [errors_simpson_integree[i] for i in indices], width, label='Simpson Intégrée')
    plt.bar(x_pos + 3.5 * width, [errors_trapeze_integree[i] for i in indices], width, label='Trapèze Intégrée')

    # Échelle logarithmique nécessaire sur l'axe Y à cause des grands écarts d'ordre de grandeur
    plt.yscale('log')

    # Configuration des étiquettes de l'axe X (affiche la valeur de n)
    plt.xticks(x_pos, [n_values[i] for i in indices])

    plt.xlabel('Nombre de segments (n)')
    plt.ylabel('Erreur absolue')
    plt.title('Comparaison des erreurs')
    plt.grid(True, axis='y', ls='--', alpha=0.7)

    # Placement de la légende à l'extérieur du graphique (à droite) pour éviter les superpositions
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')

    # Ajustement automatique des espacements pour éviter les chevauchements de textes
    plt.tight_layout()

    # --- Exportation au format PDF de la Figure 1 ---
    fig1.savefig('comparaison_methodes_integration.pdf', format='pdf', bbox_inches='tight')

    # ==========================================================
    # FIGURE 2 : ZOOM SUR LA CONVERGENCE DE SIMPSON
    # ==========================================================

    fig2 = plt.figure(figsize=(10, 6))

    # Tracé des courbes d'erreurs pour la famille de la méthode Simpson (avec marqueurs distincts)
    plt.loglog(n_values, errors_simpson_classique, 'o-c', label='Simpson Classique', linewidth=2, markersize=7)
    plt.loglog(n_values, errors_simpson_numpy, 's-m', label='Simpson NumPy', linewidth=2, markersize=7)
    plt.loglog(n_values, errors_simpson_integree, '^-', color='darkred', label='Simpson Intégrée', linewidth=2, markersize=7)

    # --- Tracé de la droite de pente théorique O(n^-4) ---
    # Calcul d'une référence basée sur le premier point pour caler la droite théorique
    ref = errors_simpson_classique[0] * (n_values[0] ** 4)
    theoretical = ref / (n_values ** 4)
    plt.loglog(n_values, theoretical, 'k--', linewidth=2, label='Pente théorique $O(n^{-4})$')

    # --- Représentation du seuil de précision machine (Machine Epsilon) ---
    # Permet de visualiser la limite basse théorique due au codage des flottants 64-bits
    plt.axhline(y=np.finfo(float).eps, color='red', linestyle=':', linewidth=2, label='Précision machine')

    # Restriction volontaire des limites de l'axe Y pour faire un focus sur le plancher de l'erreur
    plt.ylim(1e-15, 1e-14)

    plt.xlabel('Nombre de segments (n)', fontsize=12)
    plt.ylabel('Erreur absolue', fontsize=12)
    plt.title('Zoom sur la convergence de Simpson', fontsize=16, fontweight='bold')
    plt.grid(True, which="both", linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()

    # --- Exportation au format PDF de la Figure 2 ---
    fig2.savefig('zoom_convergence_simpson.pdf', format='pdf', bbox_inches='tight')

    # ==========================================================
    # RENDU FINAL DES COPIES ÉCRAN
    # ==========================================================
    plt.show()


# ==============================================================
# POINT D'ENTRÉE DU SCRIPT
# ==============================================================
if __name__ == "__main__":
    main()

