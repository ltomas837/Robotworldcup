import time
from viewer import problem as _problem, board as _board, solution as _solution
import json
from solvers.exact_solver_from_attempts import run as exact_solver_from_attempts_run
from solvers.exact_solver_from_positions import run as exact_solver_from_positions_run
from solvers.greedy_solver_from_positions import run as greedy_solver_from_positions_run
from solvers.greedy_solver_from_positions2 import run as greedy_solver_from_positions2_run
from solvers.modelisation.Graph import Graph

import numpy as np
import timeout_decorator
from copy import copy

import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import pandas as pd

solvers_to_test = {
    "exact_solver_from_attempts": exact_solver_from_attempts_run,
    "exact_solver_from_positions": exact_solver_from_positions_run,
    "greedy_solver_from_positions" : greedy_solver_from_positions_run,
    "greedy_solver_from_positions2" : greedy_solver_from_positions2_run
}

print("## Initializing problem...")
with open("viewer/configs/base_benchmark_problem.json") as problem_file:
    json_problem = json.load(problem_file)
    base_problem = _problem.Problem(json_problem)

problems_to_test = {
    "one_opponent-theta_0.0031416": base_problem,
    "three_opponents-theta_0.0031416": copy(base_problem),
    "six_opponents-theta_0.0031416": copy(base_problem),
    "one_opponent-theta_0.001": copy(base_problem),
    "one_opponent-theta_0.05": copy(base_problem),
    "six_opponents-theta_0.05": copy(base_problem),
}

problems_to_test["three_opponents-theta_0.0031416"].opponents = np.vstack((problems_to_test["three_opponents-theta_0.0031416"].opponents.transpose(),
                                                            np.array([[-2, -2], [2, 1.0]]))).transpose()
problems_to_test["six_opponents-theta_0.0031416"].opponents = np.vstack((problems_to_test["six_opponents-theta_0.0031416"].opponents.transpose(),
                                                             np.array([[-2, -2], [2, 1.0], [4.0, 2.5], [4.1, 3.0], [-4, 2.0]]))).transpose()
problems_to_test["six_opponents-theta_0.05"].opponents = problems_to_test["six_opponents-theta_0.0031416"].opponents
problems_to_test["one_opponent-theta_0.001"].theta_step = 0.001
problems_to_test["one_opponent-theta_0.05"].theta_step = 0.05
problems_to_test["six_opponents-theta_0.05"].theta_step = 0.05

##### SOLVERS BENCH ######
solvers_results = pd.DataFrame(columns=["Solveur", "Probleme", "Temps (s)"])
timeout_seconds = 60 # 1 minutes
@timeout_decorator.timeout(timeout_seconds, timeout_exception=StopIteration)
def run_solver(solver, problem):
    solver.run(problem)

for solver_name in solvers_to_test:
    current_solver = solvers_to_test[solver_name]
    for problem_name in problems_to_test:
        current_problem = problems_to_test[problem_name]
        print("Running solver {0} on the {1} benchmark problem."
              .format(solver_name, problem_name))
        start_time = time.time()
        try:
            run_solver(current_solver, current_problem)
            end_time = time.time()
            whole_time = round(end_time - start_time, 2)
        except StopIteration:
            print("{0} took more than {1} seconds to resolve {2} problem."
                  .format(solver_name, timeout_seconds, problem_name))
            whole_time = timeout_seconds

        print("{0} took {1} seconds to resolve {2} problem."
              .format(solver_name, whole_time, problem_name))
        solvers_results = solvers_results.append(pd.DataFrame({
            "Solveur": [solver_name],
            "Probleme": [problem_name],
            "Temps (s)": [whole_time]}), ignore_index=True)

chart = sns.catplot(x = "Probleme", y = "Temps (s)", hue = "Solveur",
             data = solvers_results, kind='bar', legend_out=True)
for ax in chart.axes.ravel():
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right',
        fontweight='light'
    )

plt.savefig("benchmarks/benchmark_solvers.png", bbox_inches='tight')
solvers_results.to_csv('benchmarks/benchmark_solvers2.csv', index=False)

##### GRAPH BENCH ######
graph_results = pd.DataFrame(columns=["Probleme", "Temps (s)"])
@timeout_decorator.timeout(timeout_seconds, timeout_exception=StopIteration)
def run_graph_creation(problem):
    graph = Graph(problem)

for problem_name in problems_to_test:
    current_problem = problems_to_test[problem_name]
    print("Running graph creation on the {0} benchmark problem."
          .format(problem_name))
    start_time = time.time()
    try:
        run_graph_creation(current_problem)
        end_time = time.time()
        whole_time = round(end_time - start_time, 2)
    except StopIteration:
        print("It took more than {0} seconds to create the graph for the {1} problem."
              .format(timeout_seconds, problem_name))
        whole_time = timeout_seconds

    print("It took {0} seconds to create graph on the {1} problem."
          .format(whole_time, problem_name))
    graph_results = graph_results.append(pd.DataFrame({
        "Probleme": [problem_name],
        "Temps (s)": [whole_time]}), ignore_index=True)

chart = sns.catplot(x = "Probleme", y = "Temps (s)",
             data = graph_results, kind='bar', legend_out=True, ci=None)
for ax in chart.axes.ravel():
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right',
        fontweight='light'
    )
plt.tight_layout()
plt.savefig("benchmarks/benchmark_graph.png")
graph_results.to_csv('benchmarks/benchmark_graph.csv', index=False)
