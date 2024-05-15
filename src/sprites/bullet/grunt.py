import arcade
from arcade import FACE_RIGHT, FACE_LEFT

from constants.collisions import COLLISION_ENEMY, COLLISION_GRUNT
from constants.layers import LAYER_NPC
from sprites.characters.character import Character

MASS = 1
DAMPING = 1
FRICTION = 1
ELASTICITY = 0.1

FORCE_MOVE = 20000


class Grunt(arcade.sprite.SpriteCircle, Character):
    def __init__(
            self,
            radius,
            color=arcade.csscolor.WHITE,
            soft=False,
            force_move=FORCE_MOVE
    ):
        super().__init__(radius, color=color, soft=soft)

        self.force_move = force_move

        self.sound = None
        self.alpha = 0

    def draw_debug(self):
        pass

    def draw_overlay(self):
        pass

    def update(
            self,
            delta_time,
            args
    ):

        if self.sound and not self.sound.playing:
            self.remove_from_sprite_lists()

    def setup(self, source, physics_engine, scene, state):
        # If silent there is grunt
        if state.settings.is_silent():
            self.remove_from_sprite_lists()
            return

        self.center_y = source.center_y

        if source.face == FACE_RIGHT:
            self.right = source.right + self.width * 2
        elif source.face == FACE_LEFT:
            self.force_move = -self.force_move
            self.left = source.left - self.width

        scene.add_sprite(LAYER_NPC, self)

        self.sound = state.grunt()

        physics_engine.add_sprite(
            self,
            mass=MASS,
            damping=DAMPING,
            friction=FRICTION,
            collision_type="grunt",
            elasticity=ELASTICITY
        )

        physics_engine.apply_force(self, (self.force_move, 0))
        physics_engine.add_collision_handler(COLLISION_GRUNT, COLLISION_ENEMY, post_handler=self.on_hit)

        return self

    def on_hit(self, sprite, _hit_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        self.remove_from_sprite_lists()
