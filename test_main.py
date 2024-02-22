import pytest
from main import *

def test_get_position_with_sum():
    positions = get_positions_with_sum(5)
    for p in positions:
        print(p)
        assert sum(p) == 5
        assert sorted(p) == p
        
def test_get_succ_of_position_with_roll():
    position = [1, 2, 3, 4, 5, 7]
    roll = 7
    successors = get_succ_of_position_with_roll(position, roll)
    for succ in successors:
        print(succ)
        assert sum(succ) == sum(position) - roll