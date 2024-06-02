""" Fading view """
import arcade

from views.view import View

FADE_RATE = 5


class Fading(View):
    """ Fading view """

    def __init__(self, window):
        super().__init__(window)

        self.next_view = None

        self._fade_out = None
        self._fade_in = 255
        self._do_quit = False

    def update_fade(self, next_view: arcade.View | None = None) -> None:
        """ Update fade
            @param next_view: View to show after finishing fade
        """
        if self._fade_out is not None:
            self._fade_out += FADE_RATE
            if self._fade_out is not None and self._fade_out > 255 and next_view is not None:
                self.window.show_view(next_view)

            if self._fade_out is not None and self._fade_out > 255 and self._do_quit:
                arcade.exit()

        if self._fade_in is not None:
            self._fade_in -= FADE_RATE
            if self._fade_in <= 0:
                self._fade_in = None

    def fade_out(self) -> None:
        """ Start fadeout """
        if self._fade_out is not None:
            return
        self._fade_out = 0
        self._fade_in = None

    def draw_fading(self) -> None:
        """ Draw fade overlay """
        if self._fade_out is not None:
            arcade.draw_rectangle_filled(self.window.width / 2, self.window.height / 2,
                                         self.window.width, self.window.height,
                                         (0, 0, 0, self._fade_out))

        if self._fade_in is not None:
            arcade.draw_rectangle_filled(self.window.width / 2, self.window.height / 2,
                                         self.window.width, self.window.height,
                                         (0, 0, 0, self._fade_in))

    def fade_quit(self) -> None:
        """ Fade to quit """
        self.fade_out()
        self._do_quit = True

    def fade_to_view(self, view):
        self.next_view = view
        self.fade_out()
