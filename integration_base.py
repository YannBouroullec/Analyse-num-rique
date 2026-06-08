"""
integration_base.py
====================
Socle commun du projet et premiere methode d'integration.
Convention : le vecteur de coefficients est p = [p1, p2, p3, p4].
"""

import numpy as np


def polynome(x, p):
    """Evalue f(x) = p1 + p2*x + p3*x^2 + p4*x^3.

    x peut etre un scalaire (Python pur) ou un ndarray (NumPy) : la meme ligne
    fonctionne dans les deux cas grace a la surcharge des operateurs NumPy.
    """
    p1, p2, p3, p4 = p
    return p1 + p2 * x + p3 * x ** 2 + p4 * x ** 3


def integrale_analytique(a, b, p):
    """Integrale exacte de f sur [a, b] (F(b) - F(a))."""
    p1, p2, p3, p4 = p

    def primitive(t):
        return p1 * t + p2 * t ** 2 / 2 + p3 * t ** 3 / 3 + p4 * t ** 4 / 4

    return primitive(b) - primitive(a)


def erreur(valeur_numerique, valeur_exacte):
    """Erreur absolue entre une valeur numerique et la valeur exacte."""
    return abs(valeur_numerique - valeur_exacte)


def erreur_pour_n(methode, a, b, n, p):
    """Erreur d'integration d'une methode pour un nombre de segments n.

    'methode' est une fonction methode(a, b, n, p) : on peut donc passer
    n'importe quelle methode en argument.
    """
    exacte = integrale_analytique(a, b, p)
    return erreur(methode(a, b, n, p), exacte)