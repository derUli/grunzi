""" Camera """


class Camera:
    """ Used to store top positions of screen """

    def __init__(self, x=0, y=0):
        """
        Constructor
        @param x: left
        @param y: top
        """
        self.x = x
        self.y = y

    def update(self, x, y):
        """
        Update
        @param x: left
        @param y: top
        """

        if x < 0:
            x = 0

        if y < 0:
            y = 0

        self.x, self.y = x, y

    def to_dict(self):
        """
        To dict
        @return: dictionary
        """
        return self.x, self.y

    def to_list(self):
        """
        To list
        @return: list
        """
        return [self.x, self.y]
