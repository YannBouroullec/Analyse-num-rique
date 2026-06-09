# Mini-Projet B — Intégration numérique

On calcule l'aire sous la courbe d'un polynôme de degré 3 par trois méthodes
(rectangle, trapèze, Simpson), chacune codée en Python de base puis en NumPy, et
on les compare entre elles et à des fonctions toutes faites de NumPy et SciPy. Le
but n'est pas tellement d'avoir la "meilleure" intégrale, mais de voir comment le
nombre de segments et le choix de la méthode jouent sur l'erreur et sur le temps
de calcul, et à partir de quand NumPy devient intéressant.

La fonction intégrée est `f(x) = p1 + p2*x + p3*x^2 + p4*x^3` et on cherche son
intégrale entre `a` et `b`.

## Organisation des fichiers

Le code est séparé en deux modules plus un programme principal, surtout pour
qu'on puisse travailler à trois sans se marcher dessus :

- `integration_base.py` : le socle commun (le polynôme, la solution analytique,
  les fonctions d'erreur) et la méthode des rectangles.
- `integration_methodes.py` : les trapèzes, Simpson, et les deux versions
  pré-programmées. Ce module réutilise le polynôme défini dans
  `integration_base`.
- `main.py` : fixe les paramètres, lance l'étude de convergence et les mesures de
  temps, et trace les trois figures. C'est le seul fichier à exécuter.

Les figures `fig1_convergence.png`, `fig2_temps.png` et `fig3_erreur_methodes.png`
sont produites par `main.py`. L'analyse complète est dans `rapport.pdf`.

## Pour lancer

Il faut `numpy`, `scipy` et `matplotlib` (`timeit` fait déjà partie de Python).
Sur Windows on a eu un souci classique de pip/interpréteur ; passer par `py -m
pip` règle le problème :

```
py -m pip install numpy scipy matplotlib
py main.py
```

Le programme affiche dans le terminal la valeur exacte, puis la valeur et
l'erreur de chaque méthode pour `n = 10`, et enfin le gain de NumPy par rapport à
Python. Les trois figures sont enregistrées à côté.

Pour essayer un autre polynôme ou un autre intervalle, on change les quelques
lignes en haut de `main.py` :

```python
P = [2.0, -3.0, 1.0, 2.0]   # coefficients p1, p2, p3, p4
A, B = -1.0, 2.0            # bornes de l'intégrale
N0 = 10                     # nombre de segments affiché au départ
```

## Comment marchent les méthodes

Les trois méthodes découpent `[a, b]` en `n` segments de largeur `h = (b-a)/n`.

Le **rectangle** prend la valeur de `f` au milieu de chaque segment. Le
**trapèze** relie les deux bouts du segment par une droite ; quand on somme tous
les segments, les points intérieurs sont partagés par deux segments, donc seuls
les deux bords gardent un poids `1/2`. **Simpson** fait passer une parabole par
les deux bords et le milieu, ce qui donne `(h/6)*(f(g) + 4*f(m) + f(d))` par
segment.

Chaque méthode existe en deux versions. La version Python utilise une boucle
`for` (c'est l'approche directe, proche de ce qu'on ferait en C). La version
NumPy construit le tableau de tous les points d'un coup avec `np.arange` ou
`np.linspace`, puis fait la somme en une opération, sans boucle Python.

## Quelques choix d'implémentation

Le polynôme est écrit une seule fois, dans `integration_base`, et la même ligne
sert pour un scalaire et pour un tableau NumPy : c'est la surcharge des
opérateurs de NumPy qui fait que `p2*x + p3*x**2` marche aussi bien sur un float
que sur un `ndarray`. Ça évite d'avoir deux versions du polynôme à maintenir.

Pour les fonctions d'erreur, on passe la méthode elle-même en argument
(`erreur_pour_n(methode, a, b, n, p)`). En Python une fonction est un objet comme
un autre, donc on peut ranger toutes les méthodes dans un dictionnaire (`METHODES`
dans `main.py`) et boucler dessus, au lieu de répéter le même code pour chacune.

Pour la comparaison "pré-programmée" on a pris `numpy.trapezoid` (l'ancien
`numpy.trapz`, renommé depuis NumPy 2.0) et `scipy.integrate.simpson`. Sur les
graphiques leurs courbes se superposent exactement aux nôtres, ce qui nous a
servi de vérification.

## Ce qu'on observe

Le rectangle et le trapèze voient leur erreur diminuer en `1/n^2` : doubler `n`
divise l'erreur par quatre environ. Le rectangle (point milieu) sort deux fois
plus précis que le trapèze à `n` égal, ce qui nous a un peu surpris au début mais
c'est un résultat connu.

Simpson, lui, tombe juste tout de suite : comme notre `f` est de degré 3 et que
Simpson est exact jusqu'au degré 3, son erreur reste au niveau du bruit machine
(~`1e-15`) quel que soit `n`. Augmenter `n` ne lui apporte rien.

Côté temps, NumPy n'est pas gagnant à tous les coups. À petit `n` le coût de
créer les tableaux le rend plus lent que la simple boucle Python ; le croisement
se fait vers la centaine de segments, et au-delà NumPy prend le dessus. Les
détails et les commentaires sont dans `rapport.pdf`.