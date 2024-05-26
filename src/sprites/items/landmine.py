import os
import logging
import arcade

from constants.layers import check_collision_with_layers, LAYER_NPC
from sprites.characters.character import Character
from utils.sprite import random_position

class Landmine(Character):
    def update(self, delta_time, args):

       
        difference = arcade.get_distance_between_sprites(self, args.player)

        w, h = arcade.get_window().get_size()

        if difference > h:
            return

        # TODO: handle collision with NPCs

        if arcade.check_for_collision(self, args.player):
            logging.info('TODO: Explode on collision with player')
            args.player.hurt(100)
            # TODO: Add explosion animation
            self.remove_from_sprite_lists()

def spawn_landmine(state, tilemap, scene, physics_engine):
    # Not yet implemented in Alpha Build 014
    return
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