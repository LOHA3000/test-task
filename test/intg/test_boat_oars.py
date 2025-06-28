import pytest
from boat import Boat
from gears import Oar
from exceptions import *


@pytest.mark.parametrize(
    "add_to_left, add_to_right, shift_from_left, shift_from_right, count_on_left, count_on_right",
    [(2, 3, 1, 1, 2, 3),
     (2, 3, 2, 3, 3, 2)])
def test_oar_shift(add_to_left, add_to_right,
                   shift_from_left, shift_from_right,
                   count_on_left, count_on_right):
    boat = Boat()
    boat.add_oar_to_left(add_to_left)
    boat.add_oar_to_right(add_to_right)
    boat.shift_oar_from_left(shift_from_left)
    boat.shift_oar_from_right(shift_from_right)

    assert boat.oars_on_left == count_on_left and boat.oars_on_right == count_on_right


@pytest.mark.parametrize(
    "add_to_left, add_to_right, shift_from_left, shift_from_right, exception",
    [(4, 2, 0, 0, ZeroNumberOfOars),
     (4, 2, -4, -3, NegativeNumberOfOars),
     (4, 2, 1.5, 1.0, ILLegalNumberOfOars),
     (2, 3, 3, 4, OarsOverdraft)])
def test_oar_shift_exception(add_to_left, add_to_right,
                             shift_from_left, shift_from_right,
                             exception):
    boat = Boat()
    boat.add_oar_to_left(add_to_left)
    boat.add_oar_to_right(add_to_right)
    with pytest.raises(exception):
        boat.shift_oar_from_left(shift_from_left)
    with pytest.raises(exception):
        boat.shift_oar_from_right(shift_from_right)
