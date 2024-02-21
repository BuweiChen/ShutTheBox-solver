import itertools
import sys

# Dynamic programming approach:
# Can order in non-decreasing remaining tile sums

def expected_wins(player, position, score=None):
    """calculate the expected wins of player

    Args:
        player (int): 1 or 2, indicating player 1 or 2
        position (list): list of ints representing the tiles still open on the board
        score (int, optional): for player 2 only, indicate score of player 1. Defaults to None.

    Returns:
        double representing the number of expected wins
    """
    positionSum = sum(position)
    
    # dp matrix to store expected wins for every state
    dpExpectedWins = {}
    
    for i in range (0, positionSum):
        positions = get_positions_with_sum_from_initial(i, position)
        
        for p in positions:
            pExpectedWins = 0
            succ_positionsAndPossibilities = get_next_positions_and_possibilities_from_initial(p)
            for p_succ in succ_positionsAndPossibilities:
                pExpectedWins += dpExpectedWins(p_succ[0]) * p_succ[1] 
                                    # p_succ[0] is position, a list, p_succ[1] is a probability, 
                                    # double from 0 to 1
            dpExpectedWins[i].update({p: pExpectedWins})
    
    rawExpectedWinsForPosition = 0
    succ_positionsAndPossibilities = get_next_positions_and_possibilities_from_initial(position)
    for p_succ in succ_positionsAndPossibilities:
        rawExpectedWinsForPosition += dpExpectedWins(p_succ[0]) * p_succ[1]
    
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
