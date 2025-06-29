import pytest
from boat import Boat
from states import BoatState, MoveState

    
# прямой гребок слева вращает лодку вправо
# прямой гребок справа вращает лодку влево
# обратный гребок слева вращает лодку влево
# обратный гребок справа вращает лодку вправо
    
# проверка что все направления гребков (8) отрабатывают без ошибок
# без проверки корректности состояний после них
@pytest.mark.parametrize('strokes', [
    (1, 2, 0, 0), # вперёд-лево
    (2, 2, 0, 0), # вперёд
    (2, 1, 0, 0), # вперёд-право
    (2, 0, 0, 2), # право
    (0, 0, 1, 2), # назад-право
    (0, 0, 2, 2), # назад
    (0, 0, 2, 1), # назад-лево
    (0, 2, 2, 0)  # лево
    ])
def test_strokes_all_directions(strokes):
    for move_state in (
            MoveState.drifting,
            MoveState.forward,
            MoveState.forward.heading_to_the_left,
            MoveState.forward.heading_to_the_right,
            MoveState.backward,
            MoveState.backward.heading_to_the_left,
            MoveState.backward.heading_to_the_right,
            MoveState.spin_left,
            MoveState.spin_right):
        boat = Boat((BoatState.sailing, move_state))
        boat.add_oar_to_left(2)
        boat.add_oar_to_right(2)
        
        boat.stroke(*strokes)

    
    
