from components.menu.menucomponent import SettingsComponent
from constants.quality import QUALITY_OFF, QUALITY_MEDIUM, QUALITY_HIGH
from utils.menu import make_menu, get_longest_option

MIN_SCREEN_RESOLUTION = (800, 600)


class SettingsGraphics(SettingsComponent):

    def get_blood_items(self):
        return [
            (_('Off'), QUALITY_OFF),
            (_('Medium'), QUALITY_MEDIUM),
            (_('High'), QUALITY_HIGH),
        ]

    def handle_change_blood(self, selection, selected_index):
        selected_item, index = selection
        text, value = selected_item
        self.settings_state.blood = value
        self.settings_state.apply_and_save()

    def handle_toggle_bloom(self, value):
        """ Handle toggle bloom """
        self.settings_state.bloom = value
        self.settings_state.apply_and_save()

    def handle_toggle_smoothscale(self, value):
        """ Handle toggle bloom """
        self.settings_state.smoothscale = value
        self.settings_state.apply_and_save()

    def handle_toggle_fog(self, value):
        """ Handle toggle fog """
        self.settings_state.fog = value
        self.settings_state.apply_and_save()

    def draw_menu(self, screen):
        menu = make_menu(_('Graphics'), self.settings_state.limit_fps)

        state_text = (_('Off'), _('On'))

        menu.add.dropselect(
            title=_('Blood'),
            default=self.get_selected_index(
                self.get_blood_items(),
                self.settings_state.blood),
            items=self.get_blood_items(),
            onchange=self.handle_change_blood,
            placeholder_add_to_selection_box=False,
            placeholder=get_longest_option(self.get_blood_items()),
        )

        menu.add.toggle_switch(
            _('Fog'),
            self.settings_state.fog,
            self.handle_toggle_fog,
            state_text=state_text
        )

        menu.add.toggle_switch(
            _('Bloom'),
            self.settings_state.bloom,
            self.handle_toggle_bloom,
            state_text=state_text
        )

        menu.add.toggle_switch(
            _('Smooth Scale'),
            self.settings_state.smoothscale,
            self.handle_toggle_smoothscale,
            state_text=state_text
        )

        menu.add.button(_('Back'), self.handle_back)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
