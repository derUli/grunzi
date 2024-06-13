""" Callback handlers """


class CallbackHandler:
    """ Callback handlers passed to a sprite on use """

    def __init__(self, on_complete):
        """
        Constructor
        @param on_complete: Callable
        """
        self.on_complete = on_complete
