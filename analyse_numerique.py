import numpy as np
import matplotlib.pyplot as plt
import methode_integration
import time

def main():
    # Paramètres
    p = [1, 2, 3, 4]  # 1 + 2x + 3x² + 4x³
    a, b = 0, 1
    exact_integral = methode_integration.integrale_exacte(p, a, b)

    # Valeurs de n (échelle logarithmique)
    n_values = np.logspace(1, 4, num=20, dtype=int)

    # Stockage
    errors_rectangle_classique = []
    errors_rectangle_numpy = []
    times_rectangle_classique = []
    times_rectangle_numpy = []

    for n in n_values:
        # Méthode classique
        start_time = time.perf_counter()
        approx_classique = methode_integration.methode_rectangle_classique(p, a, b, n)
        time_classique = time.perf_counter() - start_time
        error_classique = abs(approx_classique - exact_integral)

        # Méthode NumPy
        start_time = time.perf_counter()
        approx_numpy = methode_integration.methode_rectangle_numpy(p, a, b, n)
        time_numpy = time.perf_counter() - start_time
        error_numpy = abs(approx_numpy - exact_integral)

        # Vérification (les deux méthodes doivent donner le même résultat)
        assert np.isclose(approx_classique, approx_numpy, rtol=1e-10), \
            f"Résultats divergents pour n={n} : {approx_classique} vs {approx_numpy}"

        # Stockage
        errors_rectangle_classique.append(error_classique)
        errors_rectangle_numpy.append(error_numpy)
        times_rectangle_classique.append(time_classique)
        times_rectangle_numpy.append(time_numpy)

    # --- Graphiques ---
    plt.figure(figsize=(12, 10))

    # 1. Convergence (log-log)
    plt.subplot(3, 1, 1)
    plt.loglog(n_values, errors_rectangle_classique, 'b-', label='Rectangle Classique')
    plt.loglog(n_values, errors_rectangle_numpy, 'r--', label='Rectangle NumPy')
    plt.xlabel('Nombre de segments (n)')
    plt.ylabel('Erreur absolue')
    plt.title('Convergence des méthodes')
    plt.grid(True, which="both", ls="--")
    plt.legend()

    # 2. Temps de calcul (log-log)
    plt.subplot(3, 1, 2)
    plt.loglog(n_values, times_rectangle_classique, 'b-', label='Rectangle Classique')
    plt.loglog(n_values, times_rectangle_numpy, 'r--', label='Rectangle NumPy')
    plt.xlabel('Nombre de segments (n)')
    plt.ylabel('Temps (s)')
    plt.title('Temps de calcul')
    plt.grid(True, which="both", ls="--")
    plt.legend()

    # 3. Erreur par méthode (log-log, lignes au lieu de barres)
    plt.subplot(3, 1, 3)
    plt.loglog(n_values, errors_rectangle_classique, 'b-o', label='Rectangle Classique', markersize=4)
    plt.loglog(n_values, errors_rectangle_numpy, 'r--s', label='Rectangle NumPy', markersize=4)
    plt.xlabel('Nombre de segments (n)')
    plt.ylabel('Erreur absolue')
    plt.title('Erreur par méthode')
    plt.grid(True, which="both", ls="--")
    plt.legend()

    plt.tight_layout()
    plt.savefig('analyse_integration_optimisee.pdf', dpi=300)
    plt.show()

if __name__ == "__main__":
    main()