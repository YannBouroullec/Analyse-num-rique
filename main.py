"""
main.py
=======
Programme principal du Mini-Projet B (integration numerique).
Charge integration_base (socle + rectangles) et integration_methodes
(trapeze, Simpson, pre-programmees), puis compare precision et temps.
Lancer :  py main.py
"""

import timeit

import numpy as np
import matplotlib.pyplot as plt

import integration_base as base
import integration_methodes as meth


# --- Parametres (librement modifiables) ---
P = [2.0, -3.0, 1.0, 2.0]      # f(x) = 2 - 3x + x^2 + 2x^3
A, B = -1.0, 2.0               # intervalle [a, b]
N0 = 10                        # nombre de segments de depart
LISTE_N = [2 ** k for k in range(2, 19)]   # 4, 8, ..., 262144

# Nom -> fonction : on rassemble les methodes des deux modules.
METHODES = {
    "Rectangle (Python)": base.rectangle_python,
    "Rectangle (NumPy)": base.rectangle_numpy,
    "Trapeze (Python)": meth.trapeze_python,
    "Trapeze (NumPy)": meth.trapeze_numpy,
    "Simpson (Python)": meth.simpson_python,
    "Simpson (NumPy)": meth.simpson_numpy,
    "Trapeze (numpy.trapezoid)": meth.trapeze_preprog,
    "Simpson (scipy.simpson)": meth.simpson_preprog,
}


def mesure_temps(fonction, n, repetitions):
    """Temps moyen (s) d'un appel a fonction(A, B, n, P), via timeit."""
    chrono = timeit.timeit(lambda: fonction(A, B, n, P), number=repetitions)
    return chrono / repetitions


def afficher_demonstration():
    """Valeur exacte + valeur/erreur de chaque methode pour n = N0."""
    exacte = base.integrale_analytique(A, B, P)
    print("=" * 64)
    print(f"Polynome   : f(x) = {P[0]} + {P[1]}x + {P[2]}x^2 + {P[3]}x^3")
    print(f"Intervalle : [{A}, {B}]   |   n = {N0} segments")
    print(f"Integrale exacte (analytique) : {exacte:.12f}")
    print("-" * 64)
    print(f"{'Methode':32s}{'Valeur':>16s}{'Erreur':>16s}")
    print("-" * 64)
    for nom, methode in METHODES.items():
        valeur = methode(A, B, N0, P)
        err = base.erreur(valeur, exacte)
        print(f"{nom:32s}{valeur:16.8f}{err:16.2e}")
    print("=" * 64)

def etude_convergence():
    """Dict {nom_methode: liste d'erreurs} pour chaque n de LISTE_N."""
    erreurs = {nom: [] for nom in METHODES}
    for n in LISTE_N:
        for nom, methode in METHODES.items():
            erreurs[nom].append(base.erreur_pour_n(methode, A, B, n, P))
    return erreurs


def etude_temps():
    """Dict {nom_methode: liste de temps moyens} pour chaque n."""
    temps = {nom: [] for nom in METHODES}
    for n in LISTE_N:
        if n <= 1024:
            repetitions = 50
        elif n <= 100000:
            repetitions = 5
        else:
            repetitions = 3
        for nom, methode in METHODES.items():
            temps[nom].append(mesure_temps(methode, n, repetitions))
    return temps

def main():
    afficher_demonstration()
    print("\nEtude de convergence en cours...")
    erreurs = etude_convergence()
    print("Mesure des temps d'execution (timeit) en cours...")
    temps = etude_temps()
    print("\nGain de vitesse NumPy vs Python (au plus grand n) :")
    for nom_base in ["Rectangle", "Trapeze", "Simpson"]:
        t_py = temps[f"{nom_base} (Python)"][-1]
        t_np = temps[f"{nom_base} (NumPy)"][-1]
        print(f"  {nom_base:10s}: x{t_py / t_np:6.1f}   "
              f"(Python {t_py:.2e} s  vs  NumPy {t_np:.2e} s)")


if __name__ == "__main__":
    main()