import pytest
from states import *
from exceptions import *
from boat import Boat
from gears import Anchor


def test_anchor_transitions():
    boat = Boat((BoatState.sailing, MoveState.drifting), anchor=Anchor())

    boat.drop_anchor()
    assert boat.state == (BoatState.anchored, MoveState.drifting)
    
    boat.weigh_anchor()
    assert boat.state == (BoatState.sailing, MoveState.drifting)

    boat.drop_anchor()
    boat.cut_off_anchor()
    assert boat.state == (BoatState.sailing, MoveState.drifting)

    boat.add_anchor()
    boat.drop_anchor()
    boat.remove_anchor()  # за бревно зацепилось или ктулху понравился
    boat.cut_off_anchor()
    assert boat.state == (BoatState.sailing, MoveState.drifting)


def test_anchor_transitions_exception():
    boat = Boat((BoatState.sailing, MoveState.drifting))
    
    with pytest.raises(TransitionGearRequirementsError):
        boat.drop_anchor()

    boat.add_anchor()
    boat.drop_anchor()
    boat.remove_anchor()
    with pytest.raises(TransitionGearRequirementsError):
        boat.weigh_anchor()
