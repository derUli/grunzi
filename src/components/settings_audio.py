import os

import utils.audio
from components.component import Component
from constants.headup import PIGGY_PINK
from constants.quality import QUALITY_LOW
from utils.animation import Animation
from utils.helper import get_version
from utils.menu import make_menu


class SettingsAudio(Component):
    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)

        video_path = os.path.join(
            data_dir,
            'images',
            'sprites',
            'animations',
            'dancing_pig'
        )
        self.old_component = None

        self.playing = None

        # 25 Frames by second
        self.video = Animation(
            video_path,
            refresh_interval=1 / 25,
            size=self.settings_state.screen_resolution
        )

        self.menu = None

        version_file = os.path.join(self.data_dir, '..', 'VERSION')
        self.version_number = get_version(version_file)

    def draw(self, screen):
        self.draw_menu(self.screen)

    def handle_back(self):
        component = self.handle_change_component(self.old_component)
        component.video = self.video
        self.menu.disable()

    def draw_background(self):
        if self.settings_state.quality >= QUALITY_LOW:
            video_frame = self.video.get_frame()
            if video_frame:
                self.screen.blit(video_frame, (0, 0))

        self.draw_notification(self.version_number, PIGGY_PINK, self.screen)

    def handle_change_music_volume(self, range_value):
        self.settings_state.music_volume = range_value / 100
        self.settings_state.apply_and_save()

    def handle_change_sound_volume(self, range_value):
        self.settings_state.sound_volume = range_value / 100
        self.settings_state.apply_and_save()

        if self.playing and self.playing.get_busy():
            self.playing.stop()

        test_sound = os.path.join(self.data_dir, 'sounds', 'pig', 'grunt1.ogg')
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
