from states import FSMContext
from gears import Oar
from exceptions import *


class Boat:
    side_shifts = {'right': 'left', 'left': 'right'}
    
    def __init__(self, state=None, anchor=None):
        if state is None:
            state = FSMContext(self)
        else:
            state.boat = self
            
        self._state = state
        self._anchor = anchor

        self.__oars = {
            'right': [],
            'left': []}

    @property
    def has_anchor(self):
        return not self._anchor is None

    def __count_oars(self, side):
        if not side in ('left', 'right'):
            raise ILLegalBoatSideName
        
        return len(self.__oars[side])

    def __add_oar(self, side, number=1, oars=tuple()):
        if not side in ('left', 'right'):
            raise ILLegalBoatSideName
        
        if not type(number) is int:
            raise ILLegalNumberOfOars
        if number == 0:
            raise ZeroNumberOfOars
        if number < 0:
            raise NegativeNumberOfOars

        if (not (hasattr(oars, '__getitem__') and hasattr(oars, '__len__')) or
                (len(oars) and not type(oars[0]) is Oar)):
            raise ILLegalOarsListType
        
        if len(oars) < 1:
            oars = [Oar() for i in range(number)]
        else:
            number = len(oars)
            
        for i in range(number):
            new_oar = oars[i]
            self.__oars[side].append(new_oar)

    def __remove_oar(self, side, number=1):
        if not side in ('left', 'right'):
            raise ILLegalBoatSideName
        
        if not type(number) is int:
            raise ILLegalNumberOfOars
        if number == 0:
            raise ZeroNumberOfOars
        if number < 0:
            raise NegativeNumberOfOars
        if number > self.__count_oars(side):
            raise OarsOverdraft(side, self.__count_oars(side), number)
        
        removed = []
        for i in range(number):
            removed.append(self.__oars[side].pop(0))
        return removed

    def __shift_oar(self, side, number):
        if not side in ('left', 'right'):
            raise ILLegalBoatSideName
        
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
