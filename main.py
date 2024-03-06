import itertools
import sys

# global variables
N = 9
MAXSCORE = 45
dpP2 = {}
dpP2WithRoll = {}
dpP1 = {}
dpP1WithRolls = {}

def set_up():
    # precompute dice probabilities
    twoDiceSumProb = dice_probabilities()

    for p1S in range (0, MAXSCORE + 1):
        dpP2.update({p1S: {}})
        dpP2WithRoll.update({p1S: {}})
        for p2S in range (0, MAXSCORE + 1):
            positionsWithSumP2S = get_positions_with_sum(p2S)
            dice_roll_max = 12 if p2S > 6 else 6
            for p in positionsWithSumP2S:
                dpP2WithRoll[p1S].update({tuple(p): {}})
                for r in range (1, dice_roll_max + 1):
                    expected_wins = None
                    succ = get_succ_of_position_with_roll(p, r)
                    if len(succ) == 0:
                        if p2S == p1S:
                            expected_wins = 0.5
                        elif p2S < p1S:
                            expected_wins = 1
                        else:
                            expected_wins = 0    
                    else:
                        succ_value = []
                        for sc in succ:
                            succ_value.append(dpP2[p1S][tuple(sc)])
                        expected_wins = max(succ_value)
                    dpP2WithRoll[p1S][tuple(p)].update({r: expected_wins})
                    
            for p in positionsWithSumP2S:
                expected_wins = None
                if p2S < p1S: expected_wins = 1
                elif p2S >= max(7, p1S):
                    expected_wins = 0
                    for i in range (2, 13):
                        expected_wins += twoDiceSumProb[i] * dpP2WithRoll[p1S][tuple(p)][i]
                else:
                    expected_wins = 0
                    for i in range (1, 7):
                        expected_wins += 1/6 * dpP2WithRoll[p1S][tuple(p)][i]
                dpP2[p1S].update({tuple(p): expected_wins})
    
    for p1S in range (0, MAXSCORE + 1):
        positionsWithSumP1S = get_positions_with_sum(p1S)
        dice_roll_max = 12 if p2S > 6 else 6
        for p in positionsWithSumP1S:
            dpP1WithRolls.update({tuple(p): {}})
            for r in range (1, dice_roll_max + 1):
                expected_wins = None
                succ = get_succ_of_position_with_roll(p, r)
                if len(succ) == 0:
                    expected_wins = 1 - dpP2[p1S][(1,2,3,4,5,6,7,8,9)]
                else:
                    succ_value = []
                    for sc in succ:
                        succ_value.append(dpP1[tuple(sc)])
                    expected_wins = max(succ_value)
                dpP1WithRolls[tuple(p)].update({r: expected_wins})
        for p in positionsWithSumP1S:
            expected_wins = None
            if p1S == 0:
                expected_wins = 1
            elif p1S > 6:
                expected_wins = 0
                for i in range (2, 13):
                    expected_wins += twoDiceSumProb[i] * dpP1WithRolls[tuple(p)][i]
            else:
                expected_wins = 0
                for i in range (1, 7):
                    expected_wins += 1/6 * dpP1WithRolls[tuple(p)][i]
            dpP1.update({tuple(p) : expected_wins})

def dice_probabilities():
    probabilities = {}
    for i in range(1, 7):
        for j in range(1, 7):
            total = i + j
            if total in probabilities:
                probabilities[total] += 1
            else:
                probabilities[total] = 1
    total_outcomes = 36
    for key in probabilities:
        probabilities[key] /= total_outcomes
    return probabilities

def get_positions_with_sum(total_sum):
    """Generate all positions where the remaining open tiles sum to total_sum.

    Args:
        total_sum (int): Total sum of open tiles.

    Returns:
        list: List of positions, where a position is a list of ints sorted in increasing order
              representing a position where the open tiles sum to total_sum.
    """
    if total_sum == 0:
        return [[]]
    positions = []
    # Generate all possible subsets of open tiles
    for r in range(1, 10):  # Maximum possible number of tiles is 9
        for subset in itertools.combinations(range(1, 10), r):
            # Check if the sum of the subset equals the total_sum
            if sum(subset) == total_sum:
                positions.append(sorted(subset))
    return positions

def get_succ_of_position_with_roll(position, roll):
    """Generate all immediate succesors of current position by removing any number of elements
       from the current position that sums to roll

    Args:
        position (list): list of ints sorted in increasing order
        roll (int): result of the roll of a 6 sided die, or the sum of two 6 sided dice

    Returns:
        list: List of positions, where a position is a list of ints sorted in increasing order
              representing a valid successor of the current position with the current roll.
    """
    successors = []
    # Generate all possible subsets of the current position
    for r in range(len(position) + 1):
        for subset in itertools.combinations(position, r):
            # Check if the sum of the subset equals the roll
            if sum(subset) == roll:
                # Create a successor position by removing the subset from the current position
                successor = sorted(list(set(position) - set(subset)))
                successors.append(successor)
    return successors

def expected_wins(player, position, score=None):
    """calculate the expected wins of player

    Args:
        player (int): 1 or 2, indicating player 1 or 2
        position (list): list of ints representing the tiles still open on the board
        score (int, optional): for player 2 only, indicate score of player 1. Defaults to None.

    Returns:
        double representing the number of expected wins
    """
    if player == 2:
        return dpP2[score][tuple(position)]
    return dpP1[tuple(position)]

def optimal_move(player, position, roll, score=None):
    """calculate the optimal move of player

    Args:
        player (int): 1 or 2, indicating player 1 or 2
        position (list): list of ints representing the tiles still open on the board
        roll (int): value of current roll
        score (int, optional): for player 2 only, indicate score of player 1. Defaults to None.

    Returns:
        list: list of tiles to close
    """
    succ = get_succ_of_position_with_roll(position, roll)
    succ_closed_and_value = []
    best_move_and_value = None
    if player == 2:
        for sc in succ:
            succ_closed_and_value.append(list(set(position) - set(sc)), dpP2[score][tuple(sc)])
        best_move_and_value = min(succ_closed_and_value, key=(lambda x : x[1]))
    else:
        for sc in succ:
            succ_closed_and_value.append((list(set(position) - set(sc)), dpP1[tuple(sc)]))
        best_move_and_value = max(succ_closed_and_value, key=(lambda x : x[1]))
    
    return best_move_and_value[0]
    
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
    set_up()
    if action == "--expect":
        wins = expected_wins(2 if player == "--two" else 1, position, score)
        print(f"{wins:.6f}")
    elif action == "--move":
        move = optimal_move(2 if player == "--two" else 1, position, roll, score)
        print(f"{move}")
