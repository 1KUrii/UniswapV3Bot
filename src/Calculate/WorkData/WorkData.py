class WorkData:
    def __init__(self):
        self._a_name = None
        self._b_name = None
        self._list_price = None
        self._timestamp = None
        self._volume_pool = None
        self._volume_liquidity = None
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
    def volume_pool(self):
        return self._volume_pool

    @volume_pool.setter
    def volume_pool(self, value):
        self._volume_pool = value
        self.notify_observers()

    @property
    def volume_liquidity(self):
        return self._volume_liquidity

    @volume_liquidity.setter
    def volume_liquidity(self, value):
        self._volume_liquidity = value
        self.notify_observers()

    def add_observer(self, observer):
        self._observers.append(observer)
        self.notify_observers()

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()
