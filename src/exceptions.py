class ZeroNumberOfOarsError(Exception):
    def __str__(self):
        return 'Количество вёсел не может быть равным нулю'


class NegativeNumberOfOarsError(Exception):
    def __str__(self):
        return 'Количество вёсел не может быть отрицательным числом'


class ILLegalNumberOfOarsError(Exception):
    def __str__(self):
        return 'Количество вёсел не может быть ничем, кроме натурального числа типа int'


class ILLegalBoatSideNameError(Exception):
    def __str__(self):
        return 'Сторона лодки может быть задана только как правая и левая значениями ' \
               'right и left соответственно'


class ILLegalOarsListTypeError(Exception):
    def __str__(self):
        return 'Список вёсел должен быть указан как итерируемый объет, ' \
               'содержащий объекты класса gears.Oar'


class OarsOverdraftError(Exception):
    sides_locale = {'left': 'слева', 'right': 'справа'}
    
    def __init__(self, side, actual, requested):
        if side not in self.sides_locale:
            raise ILLegalBoatSideName
        if not (type(actual) is int and type(requested) is int):
            raise ValueError('Количество должно быть указано типом int')
        
        self._side = self.sides_locale[side]
        # доступны для настройки автоматизрованного управления количеством вёсел
        # например, если одно весло лодки с 6ью вёслами съел кракен, 
        # а другое сломали, отбиваясь от утопающих, причем оба с одной стороны лодки
        self._actual = actual
        self._requested = requested

    @property
    def actual(self):
        return self._actual

    @property
    def requested(self):
        return self._requested
        
    def __str__(self):
        return f'Количество вёсел {self._side} меньше - {self._actual}, '\
               f'чем указанное - {self._requested}'


class ILLegalStateTypeError(Exception):
    def __str__(self):
        return 'состояние должно быть объектом states.BaseState'


class ILLegalStatePairRepresentationError(Exception):
    def __init__(self, descriptor, state_pair):
        self._descriptor = descriptor
        self._representation = repr(state_pair)
        
    def __str__(self):
        return f'Некорректное представление состояния "{self._descriptor}": {self._representation}'


class ILLegalTransitionError(Exception):
    def __init__(self, descriptor, source):
        self._descriptor = descriptor
        self._source = source
        
    def __str__(self):
        return f'Нельзя выполнить "{self._descriptor}" из текущего состояния "{self._source}"'


class TransitionGearRequirementsError(Exception):
    def __init__(self, descriptor):
        self._descriptor = descriptor
        
    def __str__(self):
        return f'Для выполнения "{self._descriptor}" в лодке не хватает оборудования'


class InvalidAnchorTypeError(Exception):
    def __str__(self):
        return 'Якорь должен быть объектом типа gears.Anchor'


class AnchorAlreadyExistsError(Exception):
    def __str__(self):
        return 'У лодки уже есть якорь'


class NoAnchorError(Exception):    
    def __str__(self):
        return 'У лодки нет якоря'


class TransitionMethodDoesNotExistError(Exception):
    def __init__(self, descriptor):
        self._descriptor = descriptor
        
    def __str__(self):
        return f'"{self._descriptor}" не является методом смены состояния лодки'
    
