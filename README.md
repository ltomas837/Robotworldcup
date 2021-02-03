# Robotworldcup
Projects realized in the context of the curse [Algorithmique appliquée](https://www.labri.fr/perso/lhofer/index.php?page=teaching/algorithmique_appliquee/index) at Bordeaux University (M2).
This project aim to simulate the optimizaton strategies of the position of the robots participating to the [Robocup SSL](https://ssl.robocup.org/). Indeed, the Bordeaux team is the world champion of this competition.

## Prerequisites
- Python 3.6
- Pip
- Numpy
- Pygame
- Matplotlib
- Searborn
- Timeout_decorator
- Python-tk

Once you have installed python, pip is necessary to install the required libraries.
```
sudo apt install python-pip
```
Then install the required libraries with pip.
```
pip install numpy
pip install pygame
...
```
In order to install the python3-tk package, run the following command.
```
sudo apt-get install python3.6-tk
```

## How to run
The standard command to run the project is the following.
```
python main.py <problem.json> <solverName> <output_file.json>
```
See below an example.
```
python main.py viewer/configs/multigoal_problem_1.json greedy_solver_from_positions output.json
```
The following is the solution displayed.

<img src="https://github.com/ltomas837/Robotworldcup/blob/main/solution.png">

- File `benchmark.py` enables to run the solvers on different problems. The following command will run it. Note that the exact solvers are predictably slow, and the `main.py` will draw the solution from the solver.
```
python benchmark.py
```

**Note:** Warning, file `benchmark.py` uses Python library [timeout_decorator](https://pypi.org/project/timeout-decorator/) which doesn't work on Windows.
