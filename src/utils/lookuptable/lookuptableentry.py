from arcade import Sprite


class LookupTableEntry:
    """ Lookup table entry """

    def __init__(self):
        """ Constructor """

        self.position_1 = (-1, -1)
        self.position_2 = (-1, -1)
        self._value = []

    def needs_update(self, sprite1: Sprite, sprite2: Sprite = None) -> bool:
        """
        Check if the entry needs to be updated

        @param sprite1: The first sprite
        @param sprite2: The second sprite

        @return: Boolean indicating if the entry needs to be updated
        """

        check1 = sprite1.position != self.position_1

        if sprite2 is None:
            return check1

        check2 = sprite2.position != self.position_2

        return check1 or check2

    def set(self, value, sprite1: Sprite, sprite2: Sprite = None) -> None:
        """
        Set the value

        @param value: The value
        @param sprite1: The first sprite
        @param sprite2: The second sprite
        """

        self.position_1 = sprite1.position

        if sprite2 is not None:
            self.position_2 = sprite2.position

        self._value = value

    def get(self):
        """
        Get the value

        @return: Any
        """
        return self._value

    def clear(self) -> None:
        """
        Resets data
        """
        self.position_1 = (-1, -1)
        self.position_2 = (-1, -1)
        self._value = []
