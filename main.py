import itertools
import sys

# Function to calculate the probability of each dice roll
def dice_probabilities():
    return {i: 1 / 36 for i in range(2, 13)}

# Function to generate all possible subsets of a given set
def all_subsets(s):
    return itertools.chain(*map(lambda x: itertools.combinations(s, x), range(0, len(s) + 1)))

# Function to calculate the sum of a set of tiles
def sum_of_tiles(s):
    return sum(s)

# Function to calculate the expected wins for a given player and position
def expected_wins(player, position, score=None, roll=None):
    # Placeholder implementation, replace with your logic
    return 0.5

# Function to determine the optimal move for a given player and position
def optimal_move(player, position, roll):
    # Placeholder implementation, replace with your logic
    return []

if __name__ == "__main__":
    # Command line arguments
    player = sys.argv[1]
    action = sys.argv[2]
    position = list(map(int, sys.argv[3]))
    
    if player == "--two":
        score = int(sys.argv[4])
    else:
        score = None
    
    if action == "--move":
        roll = int(sys.argv[4 + (player == "--two")])
    else:
        roll = None

    # Perform action
    if action == "--expect":
        wins = expected_wins(player, position, score, roll)
        print(f"{wins:.6f}")
    elif action == "--move":
        move = optimal_move(player, position, roll)
        print(f"{move}")
