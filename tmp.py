# global variables
N = 9
MAXSCORE = 43

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
    
    # compute expected p2 wins starting turn with position and p1 score
    dpP2 = {}
    dpP2WithRoll = {}
    
    # if p1S is 0, p1 already won, so start from 1
    for p1S in range (1, MAXSCORE + 1):
        dpP2.update({p1S: {}})
        dpP2WithRoll.update({p1S: {}})
        for p2S in range (0, MAXSCORE + 1):
            positionsWithSumP2S = get_positions_with_sum(p2S)
            for p in positionsWithSumP2S:
                for r in range (1, 7):
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
                    dpP2WithRoll[p1S].update({tuple(p): expected_wins})
                    
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
