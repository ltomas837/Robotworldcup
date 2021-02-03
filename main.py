import sys
import time
from viewer import problem as _problem, board as _board, solution as _solution
import json
from solvers.exact_solver_from_attempts import run as exact_solver_from_attempts_run
from solvers.exact_solver_from_positions import run as exact_solver_from_positions_run
from solvers.greedy_solver_from_positions import run as greedy_solver_from_positions_run
from solvers.greedy_solver_from_positions2 import run as greedy_solver_from_positions2_run

solvers = {
    "exact_solver_from_attempts": exact_solver_from_attempts_run,
    "exact_solver_from_positions": exact_solver_from_positions_run,
    "greedy_solver_from_positions" : greedy_solver_from_positions_run,
    "greedy_solver_from_positions2" : greedy_solver_from_positions2_run
}

if (len(sys.argv) < 4) :
    sys.exit("Usage: " + sys.argv[0] + " <problem.json> <solverName> <output_file.json>")

problem_path = sys.argv[1]
solver_name = sys.argv[2]
output_path = sys.argv[3]

### INITIALIZATION ###
print("## Initializing solver {0}...".format(solver_name))
solver = solvers[solver_name]
if solver is None:
    sys.exit("Unknown solver")

print("## Initializing problem...")
with open(problem_path) as problem_file:
    json_problem = json.load(problem_file)
    problem = _problem.Problem(json_problem)

print("Problem used :")
print(json.dumps(json_problem, indent=4, sort_keys=True))


### SOLVING ###
print("## Starting solving...")
start_time = time.time()
solution = solver.run(problem)
end_time = time.time()
print("Found a solution with {0} defenders in {1} seconds."
      .format(len(solution.get("defenders")), round(end_time - start_time, 2)))

### EXPORT SOLUTION ###
print("## Exporting the solution as {0}...".format(output_path))
with open(output_path, 'w') as output_file:
    json.dump(solution, output_file)

### USE THE SOLUTION ###
print("## Printing the board...")
board = _board.Board(problem, _solution.Solution(solution))
board.run()

sys.exit()
