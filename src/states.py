class BaseState:
    def __init__(self, name):
        if not type(name) is str:
            raise TypeError('имя состояния должно быть указано типом str')
        
        self._name = name
        self._hierarchy = {}

    def insert_parent_name(self, parent_name):
        self._name = parent_name + ' ' + self._name

    def __str__(self):
        return self._name

    def __setattr__(self, name, value):
        if not name in ('_name', '_hierarchy'):
            if not type(value) is type(self):
                raise TypeError('состояние должно быть объектом BaseState')

            self._hierarchy[name] = value
            value.insert_parent_name(self._name)
        object.__setattr__(self, name, value)


class BoatState:
    on_land = BaseState('на суше')
    sailing = BaseState('в плавании')
    anchored = BaseState('стоит на якоре')
    moored = BaseState('пришвартована')


class MoveState:
    drifring = BaseState('дрейфует')
    
    forward = BaseState('плывёт вперёд')
    forward.heading_to_the_left = BaseState('с курсом влево')
    forward.heading_to_the_right = BaseState('с курсом вправо')
    
    backward = BaseState('плывёт назад')
    backward.heading_to_the_left = BaseState('с курсом влево')
    backward.heading_to_the_right = BaseState('с курсом вправо')
    
    aground = BaseState('на мели')
    spin_left = BaseState('повернула влево')
    spin_rigth = BaseState('повернула вправо')


class FSMContext:  # Finite State Machine
    # принимается, что скорость движения лодки - качественный показатель,
    # который может быть только в 3 горизонтально переходящих между собой состояниях:
    # вперёд <==> дрейфование <==> назад

    # принимается, что скорость вращения лодки (курс) - качественный показатель,
    # который может быть только в горизонтально переходящих между собой состояниях:
    # при движении, причём вращение меняет скорость движения на "дрейфование"
    #   вращение влево <==> курс влево <==> прямо <==> курс вправо <==> вращение вправо
    # при скорости движения "дрейфование"
    #   вращение влево <==> без вращения <==> вращение вправо

    # прямой гребок слева вращает лодку вправо
    # прямой гребок справа вращает лодку влево
    # обратный гребок слева вращает лодку влево
    # обратный гребок справа вращает лодку вправо

    def __init__(self, boat, start_boat_state=BoatState.on_land, start_move_state=MoveState.aground):
        self.boat_state = start_boat_state
        self.move_state = start_move_state
        
        # для проверки наличия оборудования в лодке
        self.boat = boat

    def change(self, heading_left, heading_right, forward, backward):
        pass
