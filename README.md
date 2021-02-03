# Algorithmique appliquée
Projet réalisé dans le cadre du cours [Algorithmique appliquée](https://www.labri.fr/perso/lhofer/index.php?page=teaching/algorithmique_appliquee/index) de Master 2 Informatique de l'Université de Bordeaux.
Ce projet vise à simuler l'optimisation de la position de robots participant à la [Robocup SSL](https://ssl.robocup.org/).

Travail réalisé par :
- Clément Romac
- Léo Tomas
- Irfaane Ousseny
- Flavien Martineau

## Prérequis
- Python 3.6
- Numpy
- Matplotlib
- Searborn

## Architecture du code
- Le dossier `viewer` contient un fork du projet [viewer](https://github.com/medrimonia/ssl_defender_viewer) fourni dans le cadre du cours.
- Le dossier `solvers` contient notre modélisation du problème et différents solveurs.
- Le fichier `main.py` permet de lancer le code pour un problème spécifié.
Pour le lancer, exécutez (ouvrir le fichier pour voir la lsite des solveurs) :
```
python main.py <problem.json> <solverName> <output_file.json>
```
- Le fichier `benchmark.py` permet de lancer le code exécutant les solveurs sur différents problèmes.
Pour le lancer, exécutez :
```
python benchmark.py
```
**Note:** Attention, le code de benchmark utilise la bibliothèque Python [timeout_decorator](https://pypi.org/project/timeout-decorator/) qui ne fonctionne pas avec Windows.

A noter que, dans le rapport final fourni, le solveur `exact_solver_from_attempts` a été exécuté séparément car il est beaucoup plus long que les autres.