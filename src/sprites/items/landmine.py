import os
import logging
import arcade
import math

from constants.layers import check_collision_with_layers, LAYER_NPC
from sprites.characters.character import Character
from utils.sprite import random_position

class Landmine(Character):
    def update(self, delta_time, args):

       
        difference = arcade.get_distance_between_sprites(self, args.player)

        w, h = arcade.get_window().get_size()
            
        if hasattr(self, 'explosion'):
            if arcade.check_for_collision(self.explosion, self.exploded_by):
                hurt = 100 / (len(self.explosion.frames) * 0.66)
                self.exploded_by.hurt(hurt)

            self.explosion.update_animation(delta_time)

            if self.explosion.cur_frame_idx >= len(self.explosion.frames) - 1:
                self.explosion.remove_from_sprite_lists()
                self.remove_from_sprite_lists()
            return

        if difference > h:
            return

        # TODO: handle collision with NPCs

        if arcade.check_for_collision(self, args.player):
            gif = arcade.load_animated_gif(os.path.join(args.state.video_dir, 'explosion.gif'))
            gif.position = self.position
            args.scene.add_sprite(LAYER_NPC, gif)
            self.explosion = gif
            self.exploded_by = args.player
            

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
