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
    n_values = np.logspace(1, 4, num=20, dtype=int)

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

        # Vérification (les deux méthodes doivent donner le même résultat)
        assert np.isclose(approx_rectangle_classique, approx_rectangle_numpy, rtol=1e-10), \
            f"Résultats divergents pour n={n} : {approx_rectangle_classique} vs {approx_rectangle_numpy}"
        assert np.isclose(approx_trapeze_classique, approx_trapeze_numpy, rtol=1e-10), \
            f"Résultats divergents pour n={n} : {approx_trapeze_classique} vs {approx_trapeze_numpy}"
        assert np.isclose(approx_simpson_classique, approx_simpson_numpy, rtol=1e-10), \
            f"Résultats divergents pour n={n} : {approx_simpson_classique} vs {approx_simpson_numpy}"

        # Stockage
        errors_rectangle_classique.append(error_rectangle_classique)
        errors_rectangle_numpy.append(error_rectangle_numpy)
        times_rectangle_classique.append(time_rectangle_classique)
        times_rectangle_numpy.append(time_rectangle_numpy)

        errors_trapeze_classique.append(error_trapeze_classique)
        errors_trapeze_numpy.append(error_trapeze_numpy)
        times_trapeze_classique.append(time_trapeze_classique)
        times_trapeze_numpy.append(time_trapeze_numpy)

        errors_simpson_classique.append(error_simpson_classique)
        errors_simpson_numpy.append(error_simpson_numpy)
        times_simpson_classique.append(time_simpson_classique)
        times_simpson_numpy.append(time_simpson_numpy)

    # --- Graphiques ---
    plt.figure(figsize=(12, 10))

    # 1. Convergence (erreur en fonction de n) - TOUTES les méthodes
    plt.subplot(3, 1, 1)
    plt.loglog(n_values, errors_rectangle_classique, 'b-', label='Rectangle Classique', linewidth=2)
    plt.loglog(n_values, errors_rectangle_numpy, 'r--', label='Rectangle NumPy', linewidth=2)
    plt.loglog(n_values, errors_trapeze_classique, 'g-', label='Trapèze Classique', linewidth=2)
    plt.loglog(n_values, errors_trapeze_numpy, 'k--', label='Trapèze NumPy', linewidth=2)
    plt.loglog(n_values, errors_simpson_classique, 'c-', label='Simpson Classique', linewidth=2)
    plt.loglog(n_values, errors_simpson_numpy, 'm--', label='Simpson NumPy', linewidth=2)
    plt.xlabel('Nombre de segments (n)')
    plt.ylabel('Erreur absolue')
    plt.title('Convergence des méthodes d\'intégration')
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend()

    # 2. Temps de calcul (temps en fonction de n) - TOUTES les méthodes
    plt.subplot(3, 1, 2)
    plt.loglog(n_values, times_rectangle_classique, 'b-', label='Rectangle Classique', linewidth=2)
    plt.loglog(n_values, times_rectangle_numpy, 'r--', label='Rectangle NumPy', linewidth=2)
    plt.loglog(n_values, times_trapeze_classique, 'g-', label='Trapèze Classique', linewidth=2)
    plt.loglog(n_values, times_trapeze_numpy, 'k--', label='Trapèze NumPy', linewidth=2)
    plt.loglog(n_values, times_simpson_classique, 'c-', label='Simpson Classique', linewidth=2)
    plt.loglog(n_values, times_simpson_numpy, 'k--', label='Simpson NumPy', linewidth=2)
    plt.xlabel('Nombre de segments (n)')
    plt.ylabel('Temps de calcul (secondes)')
    plt.title('Performance des méthodes d\'intégration')
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend()

    # 3. Erreur par méthode (barres ou courbes séparées pour chaque n) - COMPARAISON
    plt.subplot(3, 1, 3)
    # Choisir quelques valeurs de n représentatives
    n_samples = [10, 50, 100, 500, 1000, 5000]
    indices = [np.where(n_values == n)[0][0] for n in n_samples if n in n_values]

    if indices:  # Si les valeurs existent
        x_pos = np.arange(len(n_samples))
        # On réduit la largeur des barres pour que les 6 tiennent dans l'espace disponible
        width = 0.12

        errors_rect_class = [errors_rectangle_classique[i] for i in indices]
        errors_rect_np = [errors_rectangle_numpy[i] for i in indices]
        errors_trap_class = [errors_trapeze_classique[i] for i in indices]
        errors_trap_np = [errors_trapeze_numpy[i] for i in indices]
        errors_simpson_class = [errors_simpson_classique[i] for i in indices]
        errors_simpson_np = [errors_simpson_numpy[i] for i in indices]

        # On décale chaque barre d'une fraction de 'width' pour les aligner proprement
        plt.bar(x_pos - 2.5 * width, errors_rect_class, width, label='Rectangle Classique', color='tab:blue')
        plt.bar(x_pos - 1.5 * width, errors_rect_np, width, label='Rectangle NumPy', color='tab:orange')
        plt.bar(x_pos - 0.5 * width, errors_trap_class, width, label='Trapèze Classique', color='tab:green')
        plt.bar(x_pos + 0.5 * width, errors_trap_np, width, label='Trapèze NumPy', color='tab:red')
        plt.bar(x_pos + 1.5 * width, errors_simpson_class, width, label='Simpson Classique', color='tab:purple')
        plt.bar(x_pos + 2.5 * width, errors_simpson_np, width, label='Simpson NumPy', color='tab:brown')

        plt.yscale('log')
        plt.xticks(x_pos, n_samples)
        plt.xlabel('Nombre de segments (n)')
        plt.ylabel('Erreur absolue (échelle log)')
        plt.title('Comparaison des erreurs pour différentes valeurs de n')
        plt.grid(True, axis='y', ls="--", alpha=0.7)
        plt.legend()
        plt.show()

if __name__ == "__main__":
    main()
