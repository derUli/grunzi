import constants.game
from components.component import Component
import gettext
from utils.animation import Animation
import os
from utils.menu import make_menu

_ = gettext.gettext


class Settings(Component):

    def __init__(self, data_dir, handle_change_component, settings_state):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state)

        video_path = os.path.join(
            data_dir,
            'images',
            'sprites',
            'animations',
            'dancing_pig'
        )
        # 25 Frames by second
        self.video = Animation(
            video_path,
            refresh_interval=1 / 25,
            size=constants.game.SCREEN_SIZE,
            async_load=True
        )

        self.menu = None

    def update_screen(self, screen):
        self.draw_menu(self.screen)

    def handle_back(self):
        component = self.handle_change_component(None)
        component.video = self.video
        self.menu.disable()

    def draw_background(self):
        self.screen.blit(self.video.get_frame(), (0, 0))

    def handle_show_fps(self):
        self.settings_state.show_fps = not self.settings_state.show_fps
        self.settings_state.apply_and_save()
        self.refresh_menu()

    def handle_change_music_volume(self, range_value):
        self.settings_state.music_volume = range_value / 100
        self.settings_state.apply_and_save()

    def handle_toggle_fullscreen(self):
        self.settings_state.fullscreen = not self.settings_state.fullscreen
        self.settings_state.apply_and_save()
        self.refresh_menu()

    def refresh_menu(self):
        self.menu.disable()
        self.draw_menu(self.screen)

    def draw_menu(self, screen):
        menu = make_menu(_('Settings'), screen)

        fullscreen_text = _('Display Mode: ')

        if self.settings_state.fullscreen:
            fullscreen_text += _('Fullscreen')
        else:
            fullscreen_text += _('Window')

        menu.add.button(fullscreen_text, self.handle_toggle_fullscreen)

        show_fps_text = _('Show FPS: ')

        if self.settings_state.show_fps:
            show_fps_text += _('On')
        else:
            show_fps_text += _('Off')

        # menu.add.button(show_fps_text, self.handle_show_fps)

        menu.add.range_slider(
            title =_('Music Volume'), 
            default = int(self.settings_state.music_volume * 100),
            range_values = (0, 100),
            increment=10,
            value_format=lambda x: str(int(x)) + "%",
            onchange = self.handle_change_music_volume
            )

        menu.add.button(_('Back To Main Menu'), self.handle_back)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
