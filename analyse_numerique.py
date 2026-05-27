import numpy as np
import matplotlib.pyplot as plt
import methode_integration
import time


def main():
    # Paramètres
    p = [1, 2, 3, 4, 5]
    a, b = 0, 1
    exact_integral = methode_integration.integrale_exacte(p, a, b)

    # Valeurs de n (échelle logarithmique)
    # On utilise des valeurs paires pour que Simpson fonctionne de manière optimale
    n_values = np.array([10, 20, 50, 100, 200, 500, 1000, 2000, 4000, 10000], dtype=int)

    # Stockage
    errors_rectangle_classique = []
    errors_rectangle_numpy = []
    times_rectangle_classique = []
    times_rectangle_numpy = []

    errors_trapeze_classique = []
    errors_trapeze_numpy = []
    times_trapeze_classique = []
    times_trapeze_numpy = []

    errors_simpson_classique = []
    errors_simpson_numpy = []
    times_simpson_classique = []
    times_simpson_numpy = []

    errors_simpson_integree = []
    errors_trapeze_integree = []
    times_simpson_integree = []
    times_trapeze_integree = []

    for n in n_values:
        # Méthode rectangle classique
        start_time = time.perf_counter()
        approx_rectangle_classique = methode_integration.methode_rectangle_classique(p, a, b, n)
        time_rectangle_classique = time.perf_counter() - start_time
        error_rectangle_classique = abs(approx_rectangle_classique - exact_integral)

        # Méthode rectangle NumPy
        start_time = time.perf_counter()
        approx_rectangle_numpy = methode_integration.methode_rectangle_numpy(p, a, b, n)
        time_rectangle_numpy = time.perf_counter() - start_time
        error_rectangle_numpy = abs(approx_rectangle_numpy - exact_integral)

        # Méthode trapeze classique
        start_time = time.perf_counter()
        approx_trapeze_classique = methode_integration.methode_trapeze_classique(p, a, b, n)
        time_trapeze_classique = time.perf_counter() - start_time
        error_trapeze_classique = abs(approx_trapeze_classique - exact_integral)

        # Méthode trapeze numpy
        start_time = time.perf_counter()
        approx_trapeze_numpy = methode_integration.methode_trapeze_numpy(p, a, b, n)
        time_trapeze_numpy = time.perf_counter() - start_time
        error_trapeze_numpy = abs(approx_trapeze_numpy - exact_integral)

        # Méthode simpson classique
        start_time = time.perf_counter()
        approx_simpson_classique = methode_integration.methode_simpson_classique(p, a, b, n)
        time_simpson_classique = time.perf_counter() - start_time
        error_simpson_classique = abs(approx_simpson_classique - exact_integral)

        # Méthode simpson numpy
        start_time = time.perf_counter()
        approx_simpson_numpy = methode_integration.methode_simpson_numpy(p, a, b, n)
        time_simpson_numpy = time.perf_counter() - start_time
        error_simpson_numpy = abs(approx_simpson_numpy - exact_integral)

        # Méthode integree simpson (CORRIGÉ : Passage de n+1 arguments)
        start_time = time.perf_counter()
        approx_simpson_integree = methode_integration.methode_simpson_integree(p, a, b, n + 1)
        time_simpson_integree_val = time.perf_counter() - start_time
        error_simpson_integree_val = abs(approx_simpson_integree - exact_integral)

        # Méthode integree trapeze (CORRIGÉ : Passage de n+1 arguments)
        start_time = time.perf_counter()
        approx_trapeze_integree = methode_integration.methode_trapeze_integree(p, a, b, n + 1)
        time_trapeze_integree_val = time.perf_counter() - start_time
        error_trapeze_integree_val = abs(approx_trapeze_integree - exact_integral)

        # Vérification de cohérence entre versions classiques et NumPy
        assert np.isclose(approx_rectangle_classique, approx_rectangle_numpy, rtol=1e-10), \
            f"Résultats divergents pour n={n} : {approx_rectangle_classique} vs {approx_rectangle_numpy}"
        assert np.isclose(approx_trapeze_classique, approx_trapeze_numpy, rtol=1e-10), \
            f"Résultats divergents pour n={n} : {approx_trapeze_classique} vs {approx_trapeze_numpy}"
        assert np.isclose(approx_simpson_classique, approx_simpson_numpy, rtol=1e-10), \
            f"Résultats divergents pour n={n} : {approx_simpson_classique} vs {approx_simpson_numpy}"

        # Stockage des erreurs
        errors_rectangle_classique.append(error_rectangle_classique)
        errors_rectangle_numpy.append(error_rectangle_numpy)
        errors_trapeze_classique.append(error_trapeze_classique)
        errors_trapeze_numpy.append(error_trapeze_numpy)
        errors_simpson_classique.append(error_simpson_classique)
        errors_simpson_numpy.append(error_simpson_numpy)
        errors_simpson_integree.append(error_simpson_integree_val)
        errors_trapeze_integree.append(error_trapeze_integree_val)

        # Stockage des temps de calcul
        times_rectangle_classique.append(time_rectangle_classique)
        times_rectangle_numpy.append(time_rectangle_numpy)
        times_trapeze_classique.append(time_trapeze_classique)
        times_trapeze_numpy.append(time_trapeze_numpy)
        times_simpson_classique.append(time_simpson_classique)
        times_simpson_numpy.append(time_simpson_numpy)
        times_simpson_integree.append(time_simpson_integree_val)
        times_trapeze_integree.append(time_trapeze_integree_val)

    # --- Graphiques ---
    plt.figure(figsize=(12, 14))
    plt.rcParams['font.family'] = 'Arial'
    # 1. Convergence (erreur en fonction de n)
    plt.subplot(3, 1, 1)
    plt.loglog(n_values, errors_rectangle_classique, 'b-', label='Rectangle Classique', linewidth=2)
    plt.loglog(n_values, errors_rectangle_numpy, 'r--', label='Rectangle NumPy', linewidth=2)
    plt.loglog(n_values, errors_trapeze_classique, 'g-', label='Trapèze Classique', linewidth=2)
    plt.loglog(n_values, errors_trapeze_numpy, 'k--', label='Trapèze NumPy', linewidth=2)
    plt.loglog(n_values, errors_simpson_classique, 'c-', label='Simpson Classique', linewidth=2)
    plt.loglog(n_values, errors_simpson_numpy, 'm--', label='Simpson NumPy', linewidth=2)
    plt.loglog(n_values, errors_simpson_integree, color='darkred', linestyle='-', label='Simpson Intégrée', linewidth=2)
    plt.loglog(n_values, errors_trapeze_integree, color='orange', linestyle='--', label='Trapeze Intégrée', linewidth=2)
    plt.xlabel('Nombre de segments (n)')
    plt.ylabel('Erreur absolue')
    plt.title('Convergence des méthodes d\'intégration')
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend()

    # 2. Temps de calcul (temps en fonction de n)
    plt.subplot(3, 1, 2)
    plt.loglog(n_values, times_rectangle_classique, 'b-', label='Rectangle Classique', linewidth=2)
    plt.loglog(n_values, times_rectangle_numpy, 'r--', label='Rectangle NumPy', linewidth=2)
    plt.loglog(n_values, times_trapeze_classique, 'g-', label='Trapèze Classique', linewidth=2)
    plt.loglog(n_values, times_trapeze_numpy, 'k--', label='Trapèze NumPy', linewidth=2)
    plt.loglog(n_values, times_simpson_classique, 'c-', label='Simpson Classique', linewidth=2)
    plt.loglog(n_values, times_simpson_numpy, 'm--', label='Simpson NumPy', linewidth=2)
    plt.loglog(n_values, times_simpson_integree, color='darkred', linestyle='-', label='Simpson Intégrée', linewidth=2)
    plt.loglog(n_values, times_trapeze_integree, color='orange', linestyle='--', label='Trapeze Intégrée', linewidth=2)
    plt.xlabel('Nombre de segments (n)')
    plt.ylabel('Temps de calcul (secondes)')
    plt.title('Performance des méthodes d\'intégration')
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend()

    # 3. Erreur par méthode - Comparaison en barres
    plt.subplot(3, 1, 3)
    n_samples = [10, 50, 100, 500, 1000]
    indices = [np.where(n_values == n)[0][0] for n in n_samples if n in n_values]

    if indices:
        x_pos = np.arange(len(indices))
        width = 0.09

        errors_rect_class = [errors_rectangle_classique[i] for i in indices]
        errors_rect_np = [errors_rectangle_numpy[i] for i in indices]
        errors_trap_class = [errors_trapeze_classique[i] for i in indices]
        errors_trap_np = [errors_trapeze_numpy[i] for i in indices]
        errors_simpson_class = [errors_simpson_classique[i] for i in indices]
        errors_simpson_np = [errors_simpson_numpy[i] for i in indices]
        errors_simp_int = [errors_simpson_integree[i] for i in indices]
        errors_trap_int = [errors_trapeze_integree[i] for i in indices]

        # Répartition propre et symétrique des 8 barres autour de x_pos
        plt.bar(x_pos - 3.5 * width, errors_rect_class, width, label='Rectangle Classique', color='tab:blue')
        plt.bar(x_pos - 2.5 * width, errors_rect_np, width, label='Rectangle NumPy', color='tab:orange')
        plt.bar(x_pos - 1.5 * width, errors_trap_class, width, label='Trapèze Classique', color='tab:green')
        plt.bar(x_pos - 0.5 * width, errors_trap_np, width, label='Trapèze NumPy', color='tab:red')
        plt.bar(x_pos + 0.5 * width, errors_simpson_class, width, label='Simpson Classique', color='tab:purple')
        plt.bar(x_pos + 1.5 * width, errors_simpson_np, width, label='Simpson NumPy', color='tab:brown')
        plt.bar(x_pos + 2.5 * width, errors_simp_int, width, label='Simpson Intégrée', color='darkred')
        plt.bar(x_pos + 3.5 * width, errors_trap_int, width, label='Trapeze Intégrée', color='orange')

        plt.yscale('log')
        plt.xticks(x_pos, [n_values[i] for i in indices])
        plt.xlabel('Nombre de segments (n)')
        plt.ylabel('Erreur absolue (échelle log)')
        plt.title('Comparaison des erreurs pour différentes valeurs de n')
        plt.grid(True, axis='y', ls="--", alpha=0.7)
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')

    plt.tight_layout()

    # EXPORTATION EN FORMAT PDF (Le fichier sera créé dans le même dossier que ton script)
    plt.savefig('comparaison_integration_numerique.pdf', format='pdf', bbox_inches='tight')

    plt.show()


if __name__ == "__main__":
    main()
