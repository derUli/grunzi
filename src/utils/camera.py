""" Camera """


class Camera:
    """ Used to store top positions of screen """

    def __init__(self, x=0, y=0):
        """Constructor"""
        self.x = x
        self.y = y

    def update(self, x, y):
        if x < 0:
            x = 0

        if y < 0:
            y = 0

        self.x, self.y = x, y

    def to_dict(self):
        """ To dict """
        return (self.x, self.y)

    def to_list(self):
        """ To list """
        return [self.x, self.y]
