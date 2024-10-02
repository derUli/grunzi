import logging
import os
import sys

from arcade import FACE_RIGHT, FACE_LEFT, FACE_UP, FACE_DOWN

import constants.controls.controller
import constants.controls.keyboard
from constants.layers import *
from constants.maps import MAPS
from sprites.characters.player import MODIFIER_SPRINT, MODIFIER_DEFAULT
from sprites.items.item import Useable
from state.argscontainer import make_args_container
from state.savegamestate import SaveGameState
from utils.media.video import load_video, video_supported
from views.game.game import Game


class GameCampaign(Game):
    """
    Main application class.
    """

    def on_show_view(self) -> None:
        """ On show view """
        super().on_show_view()

        self.window.set_mouse_visible(False)
        self.push_controller_handlers()
        self.state.settings.unmute()

        if self.initialized:
            self.music_queue.play()
            self.atmo.play()
            return

        self.setup()

    def on_hide_view(self) -> None:
        """ On hide view """
        super().on_hide_view()

        if self.scene.player_sprite:
            self.scene.player_sprite.stop_walk()

        self.window.set_mouse_visible(True)
        self.music_queue.pause()
        self.pop_controller_handlers()
        self.atmo.pause()
        self.state.settings.mute()
        self.scene.update_scene(0, make_args_container(self))

    def setup(self) -> None:
        """ Setup game """

        video_file = os.path.join(self.state.video_dir, 'splash', f"{self.state.map_name}.webm")

        if not self.state.settings.videos or not video_supported():
            self.skip_intro = True

        if not self.skip_intro:
            self.video = load_video(
                video_file,
                self.window.size,
                self.state.settings.music_volume * self.state.settings.master_volume
            )

        super().setup()

    def on_update(self, delta_time: float) -> None:
        """Movement and game logic"""

        super().on_update(delta_time)

        self.ui.loading_screen.update(delta_time)

        if not self.initialized:
            if not self.video.active and not self.loading_music:
                self.loading_music = self.state.play_sound(
                    'loading',
                    loop=True,
                    volume=self.state.settings.music_volume * self.state.settings.master_volume,
                )
            return

        if self.video.active:
            return

        if self.loading_music:
            self.loading_music.pause()
            self.loading_music = None

        if self.atmo:
            self.atmo.update()

        if self.music_queue:
            self.music_queue.update()

        # There is an OpenGL error happening when a sprite is added by an controller event handler
        # which seems to happen because the controller events are handled in a different thread.
        # To work around this we have the _call_method class variable which can be set to a class method
        # Which is called in next execution of on_update
        if self._call_method:
            self._call_method()
            self._call_method = None

        if self.scene.player_sprite.dead and not self.level_completed:
            self.scene.player_sprite.update(delta_time, make_args_container(self))
            self.scene.player_sprite.reset()

            if not self.scene.player_sprite.bloody_screen.shown:
                self.scene.update_scene(
                    delta_time,
                    make_args_container(self)
                )

            return self.update_fade(self.next_view)

        # Move the player with the physics engine
        self.update_player_speed()
        self.physics_engine.step(delta_time)

        self.scene.update_scene(
            delta_time,
            make_args_container(self)
        )

        self.map_populator.update(make_args_container(self))

        if self.level_completed:
            self.update_fade(self.next_view, speed=2.5)
        else:
            self.update_fade(self.next_view)

    def on_draw(self) -> None:
        """Render the screen."""

        if self.video.active:
            # Loading a video will open a ffmpeg console window.
            # Which will disappear after a second.
            # The game window lose it's focus.
            # Activate the window again.
            self.window.activate()
            self.video.draw((0, 0), force_draw=True)
            return self.draw_after()

        super().on_draw()

    def on_button_press(self, controller, key):
        """ On button press """
        if self.video.active and key in constants.controls.controller.KEY_DISCARD:
            return self.video.stop()

        if not self.initialized:
            return

        if self.scene.player_sprite.dead:
            if key in constants.controls.controller.KEY_DISCARD:
                self._call_method = self.on_gameover
            return

        if key in constants.controls.controller.KEY_PAUSE:
            self._call_method = self.on_pause
        if key in constants.controls.controller.KEY_USE:
            self._call_method = self.on_use
        if key in constants.controls.controller.KEY_DROP:
            self._call_method = self.on_drop
        if key in constants.controls.controller.KEY_SHOOT:
            self._call_method = self.on_shoot
        if key in constants.controls.controller.KEY_GRUNT:
            self._call_method = self.on_grunt
        if key in constants.controls.controller.PREVIOUS_ITEM:
            self._call_method = self.on_item_previous
        if key in constants.controls.controller.NEXT_ITEM:
            self._call_method = self.on_item_next
        if key in constants.controls.controller.KEY_SPRINT:
            self.scene.player_sprite.modifier = MODIFIER_SPRINT

    def on_button_release(self, controller, key):
        if self.scene.player_sprite and key in constants.controls.controller.KEY_SPRINT:
            self.scene.player_sprite.modifier = MODIFIER_DEFAULT


    def on_gameover(self) -> None:
        """ Called when the player dies """

        self.on_next_level(same=True)

    def on_next_level(self, same=False):
        if self.next_view:
            return

        self.scene.player_sprite.reset()

        old_map = self.state.map_name
        next_map = old_map

        index = MAPS.index(old_map)

        if not same:
            self.level_completed = True
            index += 1

        completed = False

        try:
            next_map = MAPS[index]
        except IndexError:
            completed = True

        self.state.map_name = next_map

        savegame = SaveGameState.load()
        savegame.current = next_map

        if not same:
            savegame.bullet_size = self.scene.player_sprite.bullet_size

        if old_map not in savegame.completed:
            savegame.completed += [old_map]

        savegame.score[old_map] = self.state.score
        savegame.save()

        self.scene.cleanup()

        if completed:
            logging.info('Game Completed')
            from views.highscore.highscoreadd import HighscoreAdd
            self.fade_to_view(HighscoreAdd(self.window, self.state))
            return

        self.fade_to_view(GameCampaign(self.window, self.state, skip_intro=same))

    def on_stick_motion(self, controller, stick_name, x_value, y_value):
        if not self.input_ready:
            return

        x_value, y_value = round(x_value), round(y_value)

        if stick_name == constants.controls.controller.LEFTSTICK:
            if x_value > 0:
                self.state.keypressed.key_right = True
            elif x_value < 0:
                self.state.keypressed.key_left = True
            else:
                self.state.keypressed.key_right = False
                self.state.keypressed.key_left = False

            if y_value > 0:
                self.state.keypressed.key_up = True
            elif y_value < 0:
                self.state.keypressed.key_down = True
            else:
                self.state.keypressed.key_down = False
                self.state.keypressed.key_up = False

        if stick_name == constants.controls.controller.RIGHTSTICK:
            face = self.scene.player_sprite.face
            if x_value > 0:
                face = FACE_RIGHT
            if x_value < 0:
                face = FACE_LEFT
            if y_value > 0:
                face = FACE_UP
            if y_value < 0:
                face = FACE_DOWN

            self.scene.player_sprite.set_face(face)

    def on_key_press(self, key: int, modifiers: int):
        """Called whenever a key is pressed."""
        super().on_key_press(key, modifiers)

        if self.video.active and key in constants.controls.keyboard.KEY_DISCARD:
            return self.video.stop()

        if not self.initialized:
            return

        if self.scene.player_sprite.dead:
            if key in constants.controls.keyboard.KEY_DISCARD:
                return self.on_gameover()
            return

        self.state.keypressed.on_key_press(key)

        is_debug = not getattr(sys, "frozen", False)

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_pause()
        if key in constants.controls.keyboard.KEY_SPRINT:
            self.scene.player_sprite.modifier = MODIFIER_SPRINT
        if key in constants.controls.keyboard.KEY_USE:
            self.on_use()
        if is_debug and key == arcade.key.F7:
            self.on_next_level()
        if is_debug and key == arcade.key.F9:
            self.scene.kill_all_npcs()
        if key in constants.controls.keyboard.KEY_DROP:
            self.on_drop()
        if key in constants.controls.keyboard.KEY_SHOOT:
            self.on_shoot()
        if key in constants.controls.keyboard.KEY_GRUNT:
            self.on_grunt()
        if key in constants.controls.keyboard.KEY_SELECT_INVENTORY:
            self.on_select_item(key=key)
        if key in constants.controls.keyboard.KEY_PREVIOUS_ITEM:
            self.on_item_previous()
        if key in constants.controls.keyboard.KEY_NEXT_ITEM:
            self.on_item_next()

    def on_key_release(self, key: int, modifiers: int):
        """Called when the user releases a key."""

        super().on_key_release(key, modifiers)

        if not self.input_ready:
            return

        if key in constants.controls.keyboard.KEY_SPRINT:
            self.scene.player_sprite.modifier = MODIFIER_DEFAULT

        self.state.keypressed.on_key_release(key)

        if self.state.keypressed.key_pressed:
            self.update_player_speed()
        else:
            self.scene.player_sprite.stop_walk()

    def on_drop(self):
        item = self.scene.player_sprite.get_item()
        selected, index = self.ui.inventory.get_selected()

        if not item:
            logging.info('No item selected')
            return self.state.noaction()

        new_item = item.copy()
        layer = new_item.__class__.__name__

        if hasattr(new_item, 'layer_name'):
            layer = new_item.layer_name

        if check_collision_with_layers(self.scene, new_item, WALL_LAYERS):
            logging.info("Can't drop item on wall.")
            return self.state.noaction()

        if selected:
            quantity = selected.pop()

            if quantity == 0:
                self.scene.player_sprite.set_item(None)
                self.ui.inventory.unselect()

        self.scene.add_sprite(layer, new_item)

    def on_use(self):
        """ On use item """

        item = self.scene.player_sprite.get_item()
        if not item:
            if self.update_collectable():
                self.state.play_sound('coin')
                return
            else:
                interactable = self.scene.get_next_interactable()
                if interactable:
                    interactable.on_interact(args=make_args_container(self))
                    return

            self.state.noaction()
            return

        args = make_args_container(self)

        for sprite in self.scene.get_next_sprites():
            if isinstance(sprite, Useable) and arcade.check_for_collision(item, sprite):
                return item.on_use_with(
                    sprite,
                    args=args
                )

        item.on_use(
            args=make_args_container(self)
        )
