import pytest
from states import *
from exceptions import *


class BoatMock:
    def __init__(self, anchor=False):
        self.anchor = anchor

    def have_anchor(self):
        return self.anchor

    def stucked_anchor(self):
        self.anchor = False
        return True


all_transition_functions_no_gears = (
    'launch', 'get_ashore', 'run_aground', 'moor', 'unmoor', 'sail_forward', 'sail_forward_with_heading_left',
    'sail_forward_with_heading_right', 'sail_backward', 'sail_backward_with_heading_left',
    'sail_backward_with_heading_right', 'spin_left', 'spin_right', 'get_to_drift', 'cut_off_anchor')
# якорь может отсутствовать или застрять после того, как лодка встала на якорь,
# и тогда его можно отрезать, и это не требует наличия якоря
all_transition_anchor_methods = ('drop_anchor', 'weigh_anchor', 'cut_off_anchor')


@pytest.mark.parametrize(
    "source_state, avaliable_methods, destination_states",
    [((BoatState.on_land, MoveState.aground), ('launch', ),
      ((BoatState.sailing, MoveState.drifting), )),
     ((BoatState.moored, MoveState.drifting), ('unmoor', ),
      ((BoatState.sailing, MoveState.drifting), )),
     ((BoatState.sailing, MoveState.aground), ('launch', 'get_ashore'),
      ((BoatState.sailing, MoveState.drifting), (BoatState.on_land, MoveState.aground))),
     
     ((BoatState.sailing, MoveState.forward),
          ('sail_forward', 'sail_forward_with_heading_left', 'sail_forward_with_heading_right',
           'get_to_drift', 'run_aground'),
          ((BoatState.sailing, MoveState.forward),
           (BoatState.sailing, MoveState.forward.heading_to_the_left),
           (BoatState.sailing, MoveState.forward.heading_to_the_right),
           (BoatState.sailing, MoveState.drifting),
           (BoatState.sailing, MoveState.aground))),
     ((BoatState.sailing, MoveState.forward.heading_to_the_left),
          ('sail_forward', 'sail_forward_with_heading_left', 'spin_left',
           'get_to_drift', 'run_aground'),
          ((BoatState.sailing, MoveState.forward),
           (BoatState.sailing, MoveState.forward.heading_to_the_left),
           (BoatState.sailing, MoveState.spin_left),
           (BoatState.sailing, MoveState.drifting),
           (BoatState.sailing, MoveState.aground))),
     ((BoatState.sailing, MoveState.forward.heading_to_the_right),
          ('sail_forward', 'sail_forward_with_heading_right', 'spin_right',
           'get_to_drift', 'run_aground'),
          ((BoatState.sailing, MoveState.forward),
           (BoatState.sailing, MoveState.forward.heading_to_the_right),
           (BoatState.sailing, MoveState.spin_right),
           (BoatState.sailing, MoveState.drifting),
           (BoatState.sailing, MoveState.aground))),
     
     ((BoatState.sailing, MoveState.backward),
          ('sail_backward', 'sail_backward_with_heading_left', 'sail_backward_with_heading_right',
           'get_to_drift', 'run_aground'),
          ((BoatState.sailing, MoveState.backward),
           (BoatState.sailing, MoveState.backward.heading_to_the_left),
           (BoatState.sailing, MoveState.backward.heading_to_the_right),
           (BoatState.sailing, MoveState.drifting),
           (BoatState.sailing, MoveState.aground))),
     ((BoatState.sailing, MoveState.backward.heading_to_the_left),
          ('sail_backward', 'sail_backward_with_heading_left', 'spin_left',
           'get_to_drift', 'run_aground'),
          ((BoatState.sailing, MoveState.backward),
           (BoatState.sailing, MoveState.backward.heading_to_the_left),
           (BoatState.sailing, MoveState.spin_left),
           (BoatState.sailing, MoveState.drifting),
           (BoatState.sailing, MoveState.aground))),
     ((BoatState.sailing, MoveState.backward.heading_to_the_right),
          ('sail_backward', 'sail_backward_with_heading_right', 'spin_right',
           'get_to_drift', 'run_aground'),
          ((BoatState.sailing, MoveState.backward),
           (BoatState.sailing, MoveState.backward.heading_to_the_right),
           (BoatState.sailing, MoveState.spin_right),
           (BoatState.sailing, MoveState.drifting),
           (BoatState.sailing, MoveState.aground))),
     
     ((BoatState.sailing, MoveState.spin_left),
          ('spin_left', 'get_to_drift', 'run_aground'),
          ((BoatState.sailing, MoveState.spin_left),
           (BoatState.sailing, MoveState.drifting),
           (BoatState.sailing, MoveState.aground))),
     ((BoatState.sailing, MoveState.spin_right),
          ('spin_right', 'get_to_drift', 'run_aground'),
          ((BoatState.sailing, MoveState.spin_right),
           (BoatState.sailing, MoveState.drifting),
           (BoatState.sailing, MoveState.aground))),

     ((BoatState.sailing, MoveState.drifting),
          ('get_ashore', 'run_aground', 'moor', 'sail_forward', 'sail_forward_with_heading_left',
           'sail_forward_with_heading_right', 'sail_backward', 'sail_backward_with_heading_left',
           'sail_backward_with_heading_right', 'spin_left', 'spin_right'),
          ((BoatState.on_land, MoveState.aground),
           (BoatState.sailing, MoveState.aground),
           (BoatState.moored, MoveState.drifting),
           (BoatState.sailing, MoveState.forward),
           (BoatState.sailing, MoveState.forward.heading_to_the_left),
           (BoatState.sailing, MoveState.forward.heading_to_the_right),
           (BoatState.sailing, MoveState.backward),
           (BoatState.sailing, MoveState.backward.heading_to_the_left),
           (BoatState.sailing, MoveState.backward.heading_to_the_right),
           (BoatState.sailing, MoveState.spin_left),
           (BoatState.sailing, MoveState.spin_right))),
     
     ((BoatState.anchored, MoveState.drifting), ('cut_off_anchor', ),
          ((BoatState.sailing, MoveState.drifting), ))])
def test_transitions_with_exceptions(source_state, avaliable_methods, destination_states):
    unavaliable_methods = list(all_transition_functions_no_gears)
    boat = BoatMock()
    
    for method, destination_state in zip(avaliable_methods, destination_states):
        unavaliable_methods.remove(method)
        state = FSMContext(boat, *source_state)
        boat.__dict__[method]()
        assert state.state == destination_state
        
    state = FSMContext(boat, *source_state)
    for method in unavaliable_methods:
        with pytest.raises(ILLegalTransitionError):
            boat.__dict__[method]()


def test_anchor_transitions():
    boat = BoatMock(anchor=True)
    state = FSMContext(boat, BoatState.sailing, MoveState.drifting)

    boat.drop_anchor()
    assert state.state == (BoatState.anchored, MoveState.drifting)
    
    boat.weigh_anchor()
    assert state.state == (BoatState.sailing, MoveState.drifting)

    boat.drop_anchor()
    boat.cut_off_anchor()
    assert state.state == (BoatState.sailing, MoveState.drifting)

    boat.anchor = True
    boat.drop_anchor()
    boat.anchor = False
    boat.cut_off_anchor()
    assert state.state == (BoatState.sailing, MoveState.drifting)


def test_anchor_transitions_exception():
    boat = BoatMock(anchor=False)
    
    state = FSMContext(boat, BoatState.sailing, MoveState.drifting)
    with pytest.raises(TransitionGearRequirementsError):
        boat.drop_anchor()

    state = FSMContext(boat, BoatState.anchored, MoveState.drifting)
    with pytest.raises(TransitionGearRequirementsError):
        boat.weigh_anchor()
