import os

import arcade

from constants.layers import check_collision_with_layers, LAYER_NPC, LAYER_MOVEABLE
from sprites.characters.character import Character
from utils.sprite import random_position


class Landmine(Character):
    def update(self, delta_time, args):

        if hasattr(self, 'explosion'):
            self.explosion_hurt(args)

            self.explosion.update_animation(delta_time)

            if self.explosion.cur_frame_idx >= len(self.explosion.frames) - 1:
                self.explosion.remove_from_sprite_lists()
                self.remove_from_sprite_lists()
            return

        self.check_collision(args)

    def check_collision(self, args):

        difference = abs(arcade.get_distance_between_sprites(self, args.player))

        w, h = arcade.get_window().get_size()

        if difference > h:
            return

        if arcade.check_for_collision(self, args.player):
            return self.spawn_explosion(args)

        npcs = arcade.check_for_collision_with_list(self, args.scene[LAYER_NPC])

        for sprite in npcs:
            if isinstance(sprite, Character):
                return self.spawn_explosion(args)

        if any(arcade.check_for_collision_with_list(self, args.scene[LAYER_MOVEABLE])):
            self.spawn_explosion(args)

    def explosion_hurt(self, args):
        hurt = 100 / (len(self.explosion.frames) * 2.6)

        moveable = arcade.check_for_collision_with_list(self.explosion, args.scene[LAYER_MOVEABLE])

        for sprite in moveable:
            sprite.remove_from_sprite_lists()

        if arcade.check_for_collision(self.explosion, args.player):
            args.player.hurt(hurt)

        npcs = arcade.check_for_collision_with_list(self.explosion, args.scene[LAYER_NPC])

        for sprite in npcs:
            if isinstance(sprite, Character) and sprite != self:
                sprite.hurt(hurt)

    def spawn_explosion(self, args):
        gif = arcade.load_animated_gif(os.path.join(args.state.video_dir, 'explosion.gif'))
        gif.position = self.position
        self.explosion = gif

        args.scene.add_sprite(LAYER_NPC, gif)
        self.explosion.sound = args.state.play_sound('explosion')

        self.alpha = 0


def spawn_landmine(state, tilemap, scene, physics_engine):
    # Not yet implemented in Alpha Build 014
    rand_x, rand_y = random_position(tilemap)

    mine = Landmine(
        filename=os.path.join(
            state.sprite_dir,
            'traps',
            'landmine.png'
        ),
        center_x=rand_x,
        center_y=rand_y
    )

    if check_collision_with_layers(scene, mine):
        return spawn_landmine(state, tilemap, scene, physics_engine)

    scene.add_sprite(LAYER_NPC, mine)
