import pyglet.clock

from sprites.items.item import Item
from sprites.items.jeep import Jeep


CAR_SPEED = 5

class CarKey(Item):
    def on_use_with(self, b, args):
        if isinstance(b, Jeep):
            args.state.play_sound('car', 'start')
            args.player.alpha = 0

            selected, index = args.inventory.get_selected()
            if selected.pop() == 0:
                args.player.set_item(None)

            args.callbacks.on_complete()
            pyglet.clock.schedule_interval_soft(self.move_car, 1 / 72, args, b)

            return

        args.state.noaction()

    def copy(self):
        """ Copy item """
        return CarKey(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )

    def move_car(self, delta_time, args, jeep):

        jeep.center_x += CAR_SPEED

        args.player.health = 100

        if jeep.center_x >= 9500:
            self.cleanup()

    def cleanup(self):
        pyglet.clock.unschedule(self.move_car)
