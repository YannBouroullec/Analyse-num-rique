"""
integration_methodes.py
========================
Trapeze, Simpson et versions pre-programmees.
Ce module reutilise la fonction polynome definie dans integration_base.
"""

import numpy as np
from scipy.integrate import simpson as _scipy_simpson

from integration_base import polynome


def trapeze_python(a, b, n, p):
    """Methode des trapezes en Python de base."""
    h = (b - a) / n
    somme = (polynome(a, p) + polynome(b, p)) / 2.0   # bornes : poids 1/2
    for i in range(1, n):                              # noeuds interieurs : poids 1
        somme += polynome(a + i * h, p)
    return somme * h


def trapeze_numpy(a, b, n, p):
    """Methode des trapezes, vectorisee avec NumPy."""
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)        # n+1 noeuds -> n segments
    y = polynome(x, p)
    return h * (np.sum(y) - (y[0] + y[-1]) / 2.0)


def simpson_python(a, b, n, p):
    """Methode de Simpson en Python de base.

    Sur chaque segment [g, d] : (h/6)*(f(g) + 4*f(milieu) + f(d)).
    Exacte pour un polynome de degre <= 3.
    """
    h = (b - a) / n
    somme = 0.0
    for i in range(n):
        gauche = a + i * h
        droite = gauche + h
        milieu = (gauche + droite) / 2.0
        somme += polynome(gauche, p) + 4 * polynome(milieu, p) + polynome(droite, p)
    return somme * h / 6.0


def simpson_numpy(a, b, n, p):
    """Methode de Simpson, vectorisee avec NumPy."""
    h = (b - a) / n
    gauche = a + np.arange(n) * h       # bornes gauches de tous les segments
    droite = gauche + h                 # bornes droites
    milieu = gauche + h / 2.0           # milieux
    contributions = polynome(gauche, p) + 4 * polynome(milieu, p) + polynome(droite, p)
    return h / 6.0 * np.sum(contributions)


def trapeze_preprog(a, b, n, p):
    """Trapeze pre-programme : numpy.trapezoid (ex-numpy.trapz)."""
    x = np.linspace(a, b, n + 1)
    y = polynome(x, p)
    return np.trapezoid(y, x)


def simpson_preprog(a, b, n, p):
    """Simpson pre-programme : scipy.integrate.simpson."""
    x = np.linspace(a, b, n + 1)
    y = polynome(x, p)
    return _scipy_simpson(y, x=x)