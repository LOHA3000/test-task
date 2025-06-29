import pytest
from boat import Boat
from gears import Oar
from exceptions import *


@pytest.mark.parametrize(
    "add_to_left, add_to_right, remove_from_left, remove_from_right, count_on_left, count_on_right",
    [(2, 3, 1, 1, 1, 2)])
def test_oar_add_remove(add_to_left, add_to_right,
                        remove_from_left, remove_from_right,
                        count_on_left, count_on_right):
    boat = Boat()
    boat.add_oar_to_left(add_to_left)
    boat.add_oar_to_right(add_to_right)
    boat.remove_oar_from_left(remove_from_left)
    boat.remove_oar_from_right(remove_from_right)

    assert boat.oars_on_left == count_on_left and boat.oars_on_right == count_on_right


@pytest.mark.parametrize(
    "add_to_left, add_to_right, remove_from_left, remove_from_right, exception",
    [(0, 0, 0, 0, ZeroNumberOfOarsError),
     (-2, -1, -4, -3, NegativeNumberOfOarsError),
     (2.1, 3.4, 1.5, 1.0, ILLegalNumberOfOarsError)])
def test_oar_add_remove_exception(add_to_left, add_to_right,
                                  remove_from_left, remove_from_right,
                                  exception):
    boat = Boat()
    with pytest.raises(exception):
        boat.add_oar_to_left(add_to_left)
    with pytest.raises(exception):
        boat.add_oar_to_right(add_to_right)
    with pytest.raises(exception):
        boat.remove_oar_from_left(remove_from_left)
    with pytest.raises(exception):
        boat.remove_oar_from_right(remove_from_right)


@pytest.mark.parametrize(
    "add_to_left, add_to_right, count_on_left, count_on_right",
    [([Oar(), Oar()], tuple(), 2, 1)])
def test_oar_add_group(add_to_left, add_to_right, count_on_left, count_on_right):
    boat = Boat()
    boat.add_oar_to_left(oars=add_to_left)
    boat.add_oar_to_right(oars=add_to_right)

    assert boat.oars_on_left == count_on_left and boat.oars_on_right == count_on_right


@pytest.mark.parametrize(
    "add_to_left, add_to_right, exception",
    [(['весло', ...], [42, 13], ILLegalOarsListTypeError),
     (..., {Oar()}, ILLegalOarsListTypeError)])
def test_oar_add_group_exception(add_to_left, add_to_right, exception):
    boat = Boat()
    with pytest.raises(exception):
        boat.add_oar_to_left(oars=add_to_left)
    with pytest.raises(exception):
        boat.add_oar_to_right(oars=add_to_right)
