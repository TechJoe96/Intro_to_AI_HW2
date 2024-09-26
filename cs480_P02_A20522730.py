import sys
import csp_A20522730
import board_A20522730
import time

# python cs480_P02_A20522730.py 2 testcase4.csv

if len(sys.argv) != 3:  # Including the script name, we expect 3 arguments in total
    print("Error: Incorrect number of arguments provided.")
    sys.exit(1)

# Check if the algorithm selection is valid
elif sys.argv[1] not in ["1", "2", "3", "4"]:
    print("Error: Invalid algorithm selection.")
    sys.exit(1)

# Extract the arguments
ALGO = sys.argv[1]  # string: either 1, 2, 3 or 4
INP = sys.argv[2]  # csv file name

# Assign algorithm names based on the selection
if ALGO == "1":
    ALGO_name = "brute force search"
elif ALGO == "2":
    ALGO_name = "Constraint Satisfaction Problem back-tracking search"
elif ALGO == "3":
    ALGO_name = "CSP with forward-checking and MRV heuristics search"
elif ALGO == "4":
    ALGO_name = "test of the completed puzzle is correct"


board_obj = board_A20522730.Board()
puzzle = board_obj.read_sudoku_csv(INP)
csp_obj = csp_A20522730.SudokuCSP(puzzle)

print("Youngjo, Choi, A20522730 solution:")
print(f"Input file: {INP}")
print(f"Algorithm: {ALGO_name}")
print("Input puzzle:")
board_obj.display_board(puzzle)

assignment = [row[:] for row in puzzle]
solution = None

# Start the timer
if ALGO != "4":
    timeStart = time.time()

if ALGO == "1":  # brute force
    solution = csp_obj.brute_force_search(puzzle)
elif ALGO == "2":  # CSP back-tracking search
    solution = csp_obj.backtrack_mode2(assignment)
elif ALGO == "3":  # CSP with forward-checking & MRV heuristics
    # In your main function or wherever you are calling the CSP solver
    domains = csp_obj.initialize_domains(puzzle)
    solution = csp_obj.backtrack_mode3(assignment, domains)
elif ALGO == "4":  # test
    solution = puzzle  # Assuming the puzzle input is the completed puzzle
    is_correct = csp_obj.is_puzzle_correct(solution)
    # Determine the correctness of the puzzle
    if is_correct:
        print("This is valid, solved, Sudoku puzzle.")
    else:
       print("ERROR: This is NOT a solved Sudoku puzzle.")

# Stop the timer
if ALGO != "4":
    timeEnd = time.time()
    elapsedTimeInSec = timeEnd - timeStart

    print(f"Number of search tree nodes generated: {csp_obj.nodes_generated}")
    print(f"Search time: {elapsedTimeInSec:.5f} seconds")

    if solution:
        print("Solved puzzle:")
        board_obj.display_board(solution)
    else:
        print("No solution found")
