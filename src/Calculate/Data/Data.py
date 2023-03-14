from enum import Enum


class Token(Enum):
    USDT = 1
    PAIR = 0


class Data:
    def __init__(self):
        self._a_name = None
        self._b_name = None
        self._list_price = None
        self._timestamp = None
        self._volume = None
        self._observers = []

    @property
    def a_name(self):
        return self._a_name

    @a_name.setter
    def a_name(self, value):
        self._a_name = value
        self.notify_observers()

    @property
    def b_name(self):
        return self._b_name

    @b_name.setter
    def b_name(self, value):
        self._b_name = value
        self.notify_observers()

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value
        self.notify_observers()

    @property
    def list_price(self):
        return self._list_price

    @list_price.setter
    def list_price(self, value):
        self._list_price = value
        self.notify_observers()

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        self.notify_observers()

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()
