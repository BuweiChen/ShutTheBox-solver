import itertools
import sys

# global variables
N = 9
MAXSCORE = 43

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

def expected_wins(player, position, score=None):
    """calculate the expected wins of player

    Args:
        player (int): 1 or 2, indicating player 1 or 2
        position (list): list of ints representing the tiles still open on the board
        score (int, optional): for player 2 only, indicate score of player 1. Defaults to None.

    Returns:
        double representing the number of expected wins
    """
    
    # precompute dice probabilities
    twoDiceSumProb = dice_probabilities()
    
    # start with player 2 end states
    
    # will need to merge the following 2 loops for DP
    
    # compute expected p2 wins starting turn with position, roll, and p1 score
    dpP2WithRoll = {}
    for p1S in range (0, MAXSCORE + 1):
        dpP2WithRoll.update({p1S: {}})
        for p2S in range (0, MAXSCORE + 1):
            positionsWithSumP2S = get_positions_with_sum(p2S)
            for r in range (1, 7):
                for p in positionsWithSumP2S:
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
                            succ_value.append(dpP2[p1S][tuple(p)])
                        expected_wins = max(succ_value)
                    dpP2WithRoll[p1S].update({tuple(p): expected_wins})
    
    # compute expected p2 wins starting turn with position and p1 score
    dpP2 = {}
    for p1S in range (0, MAXSCORE + 1):
        dpP2.update({p1S: {}})
        for p2S in range (0, MAXSCORE + 1):
            positionsWithSumP2S = get_positions_with_sum(p2S)
            for p in positionsWithSumP2S:
                expected_wins = None
                if p2S < p1S: expected_wins = 1
                elif p2S >= max(7, p1S):
                    expected_wins = 0
                    for i in range (2, 13):
                        expected_wins += twoDiceSumProb[i] * dpP2WithRoll[p1S][i][tuple(p)]
                else:
                    expected_wins = 0
                    for i in range (1, 7):
                        expected_wins += 1/6 * dpP2WithRoll[p1S][i][tuple(p)]
                dpP2[p1S].update({tuple(p): expected_wins})
    pass
    

def optimal_move(player, position, roll, score=None):
    """calculate the optimal move of player

    Args:
        player (int): 1 or 2, indicating player 1 or 2
        position (list): list of ints representing the tiles still open on the board
        roll (int): value of current roll
        score (int, optional): for player 2 only, indicate score of player 1. Defaults to None.

    Returns:
        _type_: _description_
    """
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
