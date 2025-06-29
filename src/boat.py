from states import FSMContext
from gears import Oar, Anchor
from exceptions import *


class Boat:
    side_shifts = {'right': 'left', 'left': 'right'}
    
    def __init__(self, initial_state=None, anchor=None):
        if initial_state is None:
            state = FSMContext(self)
        else:
            state = FSMContext(self, *initial_state)
            
        self._state = state
        self._anchor = None
        if not anchor is None:
            self.add_anchor(anchor)

        self._oars = {
            'right': [],
            'left': []}

    def add_anchor(self, anchor=None):
        if not self._anchor is None:
            raise AnchorAlreadyExistsError
            
        if anchor is None:
            anchor = Anchor()
        elif not type(anchor) is Anchor:
            raise InvalidAnchorTypeError
            
        self._anchor = anchor

    def remove_anchor(self):
        if self._anchor is None:
            raise NoAnchorError
            
        self._anchor = None

    def have_anchor(self):
        return not self._anchor is None

    def stucked_anchor(self):
        self._anchor = None
        return True

    def __count_oars(self, side):
        if not side in ('left', 'right'):
            raise ILLegalBoatSideNameError
        
        return len(self._oars[side])

    def __add_oar(self, side, number=1, oars=tuple()):
        if not side in ('left', 'right'):
            raise ILLegalBoatSideNameError
        
        if not type(number) is int:
            raise ILLegalNumberOfOarsError
        if number == 0:
            raise ZeroNumberOfOarsError
        if number < 0:
            raise NegativeNumberOfOarsError

        if (not (hasattr(oars, '__getitem__') and hasattr(oars, '__len__')) or
                (len(oars) and not type(oars[0]) is Oar)):
            raise ILLegalOarsListTypeError
        
        if len(oars) < 1:
            oars = [Oar() for i in range(number)]
        else:
            number = len(oars)
            
        for i in range(number):
            new_oar = oars[i]
            self._oars[side].append(new_oar)

    def __remove_oar(self, side, number=1):
        if not side in ('left', 'right'):
            raise ILLegalBoatSideNameError
        
        if not type(number) is int:
            raise ILLegalNumberOfOarsError
        if number == 0:
            raise ZeroNumberOfOarsError
        if number < 0:
            raise NegativeNumberOfOarsError
        if number > self.__count_oars(side):
            raise OarsOverdraftError(side, self.__count_oars(side), number)
        
        removed = []
        for i in range(number):
            removed.append(self._oars[side].pop(0))
        return removed

    def __shift_oar(self, side, number):
        if not side in ('left', 'right'):
            raise ILLegalBoatSideNameError
        
        shift_from_side = side
        shift_to_side = self.side_shifts[side]
        
        oars_on_shift = self.__remove_oar(shift_from_side, number)
        self.__add_oar(shift_to_side, oars=oars_on_shift)

    @property
    def oars_on_right(self):
        return self.__count_oars('right')
    
    @property
    def oars_on_left(self):
        return self.__count_oars('left')

    def add_oar_to_right(self, number=1, oars=tuple()):
        self.__add_oar('right', number, oars)

    def add_oar_to_left(self, number=1, oars=tuple()):
        self.__add_oar('left', number, oars)

    def remove_oar_from_right(self, number=1):
        return self.__remove_oar('right', number)
            
    def remove_oar_from_left(self, number=1):
        return self.__remove_oar('left', number)

    def shift_oar_from_right(self, number=1):
        self.__shift_oar('right', number)

    def shift_oar_from_left(self, number=1):
        self.__shift_oar('left', number)

    @property
    def state(self):
        return self._state.state

    @property
    def state_as_string(self):
        return ', '.join(map(str, self._state.state))

    def stroke(self, number_stright_left=0, number_stright_right=0,
               number_reverse_left=0, number_reverse_right=0):
        
        if number_stright_left < 0:
            raise NegativeNumberOfOarsError
        if number_stright_right < 0:
            raise NegativeNumberOfOarsError
        if number_reverse_left < 0:
            raise NegativeNumberOfOarsError
        if number_reverse_right < 0:
            raise NegativeNumberOfOarsError

        if number_stright_left + number_reverse_left > self.oars_on_left:
            raise OarsOverdraftError('left', self.oars_on_left, number_stright_left + number_reverse_left)
        elif number_stright_right + number_reverse_right > self.oars_on_right:
            raise OarsOverdraftError('right', self.oars_on_right, number_stright_right + number_reverse_right)

        # прямой гребок слева вращает лодку вправо
        # прямой гребок справа вращает лодку влево
        # обратный гребок слева вращает лодку влево
        # обратный гребок справа вращает лодку вправо

        heading_left = number_stright_right + number_reverse_left
        heading_right = number_stright_left + number_reverse_right

        forward = number_stright_left + number_stright_right
        backward = number_reverse_left + number_reverse_right

        self._state.change(heading_left, heading_right, forward, backward)
