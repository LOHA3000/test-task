class ZeroNumberOfOars(Exception):
    def __str__(self):
        return 'Количество вёсел не может быть равным нулю'


class NegativeNumberOfOars(Exception):
    def __str__(self):
        return 'Количество вёсел не может быть отрицательным числом'


class ILLegalNumberOfOars(Exception):
    def __str__(self):
        return 'Количество вёсел не может быть ничем, кроме натурального числа типа int'


class ILLegalBoatSideName(Exception):
    def __str__(self):
        return 'Сторона лодки может быть задана только как правая и левая значениями ' \
               'right и left соответственно'


class ILLegalOarsListType(Exception):
    def __str__(self):
        return 'Список вёсел должен быть указан как итерируемый объет, ' \
               'содержащий объекты класса Oar'


class OarsOverdraft(Exception):
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
