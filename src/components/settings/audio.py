import os

import utils.audio
from components.menucomponent import SettingsComponent
from utils.helper import get_version
from utils.menu import make_menu


class SettingsAudio(SettingsComponent):
    def __init__(self, data_dir, handle_change_component,
                 settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(
            data_dir,
            handle_change_component,
            settings_state,
            enable_edit_mode,
            gamepad
        )

        self.playing = None

        version_file = os.path.join(self.data_dir, '..', 'VERSION')
        self.version_number = get_version(version_file)

    def handle_change_music_volume(self, range_value):
        self.settings_state.music_volume = range_value / 100
        self.settings_state.apply_and_save()

    def handle_change_sound_volume(self, range_value):
        self.settings_state.sound_volume = range_value / 100
        self.settings_state.apply_and_save()

        if self.playing and self.playing.get_busy():
            self.playing.stop()

        test_sound = os.path.join(self.data_dir, 'sounds', 'pig', 'grunt4.ogg')
        self.playing = utils.audio.play_sound(test_sound)

    def draw_menu(self, screen):
        menu = make_menu(_('Audio'), self.settings_state.limit_fps)

        menu.add.range_slider(
            title=_('Music'),
            default=int(self.settings_state.music_volume * 100),
            range_values=(0, 100),
            increment=10,
            value_format=lambda x: str(int(x)) + "%",
            onchange=self.handle_change_music_volume
        )

        menu.add.range_slider(
            title=_('Sound Effects'),
            default=int(self.settings_state.sound_volume * 100),
            range_values=(0, 100),
            increment=10,
            value_format=lambda x: str(int(x)) + "%",
            onchange=self.handle_change_sound_volume
        )

        menu.add.button(_('Back'), self.handle_back)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
