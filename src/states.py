from exceptions import *


class BaseState:
    def __init__(self, name):
        if not type(name) is str:
            raise ILLegalStateTypeError
        
        self._name = name
        self._hierarchy = {}
        self._group_name = ''
        self._descriptor_name = ''

    def insert_parent_name(self, parent_name):
        self._name = parent_name + ' ' + self._name

    def __str__(self):
        return self._name

    def __repr__(self):
        return ' '.join((self._group_name, self._descriptor_name,))

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            if not type(value) is type(self):
                raise ILLegalStateTypeError

            self._hierarchy[name] = value
            value.insert_parent_name(self._name)
        object.__setattr__(self, name, value)

    def __set_name__(self, owner, name):
        self._group_name = repr(owner)
        self._descriptor_name = name
        for name, value in self._hierarchy.items():
            value.__set_name__(self, name)


class BoatState:
    on_land = BaseState('на суше')
    sailing = BaseState('в плавании')
    anchored = BaseState('стоит на якоре')
    moored = BaseState('пришвартована')


class MoveState:
    drifting = BaseState('дрейфует')

    # курс определяется по направлению носа лодки
    
    forward = BaseState('плывёт вперёд')
    forward.heading_to_the_left = BaseState('с курсом влево')
    forward.heading_to_the_right = BaseState('с курсом вправо')
    
    backward = BaseState('плывёт назад')
    backward.heading_to_the_left = BaseState('с курсом влево')
    backward.heading_to_the_right = BaseState('с курсом вправо')
    
    aground = BaseState('на мели')
    
    spin_left = BaseState('вращается влево')
    spin_right = BaseState('вращается вправо')


class Transition:
    def __init__(self, context, descriptor, source, destination, case=(lambda: True)):
        if len(source) < 2:
            raise ILLegalStatePairRepresentationError(descriptor, source)
        if len(destination) < 2:
            raise ILLegalStatePairRepresentationError(descriptor, destination)
        if not (hasattr(source[0], '__getitem__') and hasattr(source[0], '__len__')):
            source = (source, )
        try:
            for source_boat, source_move in source:
                 if not (isinstance(source_boat, BaseState) and isinstance(source_move, BaseState)):
                     raise ILLegalStateTypeError
            destination_boat, destination_move = destination
            if not (isinstance(destination_boat, BaseState) and isinstance(destination_move, BaseState)):
                raise ILLegalStateTypeError
        except (ValueError):
            raise ILLegalStateTypeError
        self._source = source
        self._destination = destination
        self._case = case
        self._context = context
        self._descriptor = descriptor

    def __call__(self):
        if not self._case():
            raise TransitionGearRequirementsError(self._descriptor)
        if not self._context.state in self._source:
            raise ILLegalTransitionError(self._descriptor, self._context.state)

        self._context.boat_state, self._context.move_state = self._destination


class FSMContext:  # Finite State Machine
    # принимается, что скорость движения лодки - качественный показатель,
    # который может быть только в 3 горизонтально переходящих между собой состояниях:
    # вперёд <==> дрейфование <==> назад

    # принимается, что скорость вращения лодки (курс) - качественный показатель,
    # который может быть только в горизонтально переходящих между собой состояниях:
    # при движении, причём вращение меняет скорость движения на "дрейфование"
    #   вращение влево <== курс влево <==> прямо <==> курс вправо ==> вращение вправо
    # при скорости движения "дрейфование"
    #   вращение влево <==> без вращения <==> вращение вправо

    # прямой гребок слева вращает лодку вправо
    # прямой гребок справа вращает лодку влево
    # обратный гребок слева вращает лодку влево
    # обратный гребок справа вращает лодку вправо

    def __init__(self, boat, start_boat_state=BoatState.on_land, start_move_state=MoveState.aground):
        if not (isinstance(start_boat_state, BaseState) and isinstance(start_move_state, BaseState)):
             raise ILLegalStateTypeError

        self.boat_state = start_boat_state
        self.move_state = start_move_state
        
        # для проверки наличия оборудования в лодке
        self._boat = boat

        self._init_transitions()

    @property
    def state(self):
        return self.boat_state, self.move_state

    def _init_transitions(self):
        transitions = (
            ('launch', ((BoatState.on_land, MoveState.aground),
                        (BoatState.sailing, MoveState.aground)),
                 (BoatState.sailing, MoveState.drifting), None),
            ('get_ashore', ((BoatState.sailing, MoveState.drifting),
                            (BoatState.sailing, MoveState.aground)),
                 (BoatState.on_land, MoveState.aground), None),
            ('run_aground', ((BoatState.sailing, MoveState.drifting),
                             (BoatState.sailing, MoveState.forward),
                             (BoatState.sailing, MoveState.forward.heading_to_the_left),
                             (BoatState.sailing, MoveState.forward.heading_to_the_right),
                             (BoatState.sailing, MoveState.backward),
                             (BoatState.sailing, MoveState.backward.heading_to_the_left),
                             (BoatState.sailing, MoveState.backward.heading_to_the_right),
                             (BoatState.sailing, MoveState.spin_left),
                             (BoatState.sailing, MoveState.spin_right)),
                 (BoatState.sailing, MoveState.aground), None),
            ('moor', (BoatState.sailing, MoveState.drifting), (BoatState.moored, MoveState.drifting), None),
            ('unmoor', (BoatState.moored, MoveState.drifting), (BoatState.sailing, MoveState.drifting), None),
            ('sail_forward', ((BoatState.sailing, MoveState.drifting),
                              (BoatState.sailing, MoveState.forward),
                              (BoatState.sailing, MoveState.forward.heading_to_the_left),
                              (BoatState.sailing, MoveState.forward.heading_to_the_right)),
                 (BoatState.sailing, MoveState.forward), None),
            ('sail_forward_with_heading_left', ((BoatState.sailing, MoveState.drifting),
                                                (BoatState.sailing, MoveState.forward),
                                                (BoatState.sailing, MoveState.forward.heading_to_the_left)),
                 (BoatState.sailing, MoveState.forward.heading_to_the_left), None),
            ('sail_forward_with_heading_right', ((BoatState.sailing, MoveState.drifting),
                                                 (BoatState.sailing, MoveState.forward),
                                                 (BoatState.sailing, MoveState.forward.heading_to_the_right)),
                 (BoatState.sailing, MoveState.forward.heading_to_the_right), None),
            ('sail_backward', ((BoatState.sailing, MoveState.drifting),
                               (BoatState.sailing, MoveState.backward),
                               (BoatState.sailing, MoveState.backward.heading_to_the_left),
                               (BoatState.sailing, MoveState.backward.heading_to_the_right)),
                 (BoatState.sailing, MoveState.backward), None),
            ('sail_backward_with_heading_left', ((BoatState.sailing, MoveState.drifting),
                                                 (BoatState.sailing, MoveState.backward),
                                                 (BoatState.sailing, MoveState.backward.heading_to_the_left)),
                 (BoatState.sailing, MoveState.backward.heading_to_the_left), None),
            ('sail_backward_with_heading_right', ((BoatState.sailing, MoveState.drifting),
                                                  (BoatState.sailing, MoveState.backward),
                                                  (BoatState.sailing, MoveState.backward.heading_to_the_right)),
                 (BoatState.sailing, MoveState.backward.heading_to_the_right), None),
            ('spin_left', ((BoatState.sailing, MoveState.drifting),
                           (BoatState.sailing, MoveState.forward.heading_to_the_left),
                           (BoatState.sailing, MoveState.backward.heading_to_the_left),
                           (BoatState.sailing, MoveState.spin_left)),
                 (BoatState.sailing, MoveState.spin_left), None),
            ('spin_right', ((BoatState.sailing, MoveState.drifting),
                            (BoatState.sailing, MoveState.forward.heading_to_the_right),
                            (BoatState.sailing, MoveState.backward.heading_to_the_right),
                            (BoatState.sailing, MoveState.spin_right)),
                 (BoatState.sailing, MoveState.spin_right), None),
            ('get_to_drift', ((BoatState.sailing, MoveState.forward),
                              (BoatState.sailing, MoveState.forward.heading_to_the_left),
                              (BoatState.sailing, MoveState.forward.heading_to_the_right),
                              (BoatState.sailing, MoveState.backward),
                              (BoatState.sailing, MoveState.backward.heading_to_the_left),
                              (BoatState.sailing, MoveState.backward.heading_to_the_right),
                              (BoatState.sailing, MoveState.spin_left),
                              (BoatState.sailing, MoveState.spin_right)),
                 (BoatState.sailing, MoveState.drifting), None),
            ('drop_anchor', (BoatState.sailing, MoveState.drifting),
                 (BoatState.anchored, MoveState.drifting), self._boat.have_anchor),
            ('weigh_anchor', (BoatState.anchored, MoveState.drifting),
                 (BoatState.sailing, MoveState.drifting), self._boat.have_anchor),
            ('cut_off_anchor', (BoatState.anchored, MoveState.drifting),
                 (BoatState.sailing, MoveState.drifting), self._boat.stucked_anchor))
        for descriptor, boat_state_from, boat_state_to, case in transitions:
            if case:
                self._boat.__setattr__(descriptor, Transition(
                    self, descriptor, boat_state_from, boat_state_to, case))
            else:
                self._boat.__setattr__(descriptor, Transition(
                    self, descriptor, boat_state_from, boat_state_to))

    def change(self, heading_left, heading_right, forward, backward):
        if (self.boat_state in (BoatState.on_land, BoatState.anchored, BoatState.moored) or
                self.move_state == MoveState.aground):
            return
