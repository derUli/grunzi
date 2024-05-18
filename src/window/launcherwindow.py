import logging
import os
import sys
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk

from PIL.ImageTk import PhotoImage
from shell import shell
from ttkthemes import ThemedTk

from constants.audio import AUDIO_BACKENDS
from state.settingsstate import SettingsState
from utils.path import is_windows, get_autodetect_path
from utils.screen import supported_screen_resolutions

NOTEBOOK_PADDING = 20

SPACE_BETWEEN = 2

TTK_THEME = 'equilux'


class LauncherWindow(ThemedTk):
    def __init__(self, theme=TTK_THEME, args=None, state=None):
        super().__init__(theme=theme)

        self.path_state = state
        self.args = args

        self.fullscreen = tk.BooleanVar(value=args.fullscreen)
        self.screen_resolution = tk.StringVar(
            value=str(args.width) + 'x' + str(args.height)
        )

        self.vsync = tk.BooleanVar(value=not args.no_vsync)
        self.borderless = tk.BooleanVar(value=args.borderless)

        true_val = True
        self.traffic = tk.BooleanVar(value=true_val)
        self.sky = tk.BooleanVar(value=true_val)
        self.shaders = tk.BooleanVar(value=true_val)
        self.videos = tk.BooleanVar(value=true_val)

        self.antialiasing = tk.StringVar(value=_('Medium'))

        self.audio_backend = tk.StringVar(value=args.audio_backend)
        self.state = SettingsState()
        self.confirmed = False
        self.borderless_check = None

    def setup(self) -> None:
        """
        Set up the UI
        """
        self.title(_('Grunzi'))
        self.bind_keyevents()
        self.set_icon()

        if SettingsState.exists():
            self.state = SettingsState.load()

            self.fullscreen.set(self.state.fullscreen)
            self.vsync.set(self.state.vsync)
            self.borderless.set(self.state.borderless)
            self.antialiasing.set(self.value_to_selected_antialiasing(self.state.antialiasing))

            self.sky.set(self.state.sky)
            self.traffic.set(self.state.traffic)
            self.shaders.set(self.state.shaders)
            self.videos.set(self.state.videos)

            w, h = self.state.screen_resolution[0], self.state.screen_resolution[1]
            self.screen_resolution.set(
                value=str(w) + 'x' + str(h)
            )

            self.audio_backend.set(self.state.audio_backend)

        tab_control = ttk.Notebook(self)

        tab_display = ttk.Frame(tab_control, padding=NOTEBOOK_PADDING)
        tab_graphics = ttk.Frame(tab_control, padding=NOTEBOOK_PADDING)
        tab_audio = ttk.Frame(tab_control, padding=NOTEBOOK_PADDING)

        tab_control.add(tab_display, text=_('Display'))
        tab_control.add(tab_graphics, text=_('Graphics'))
        tab_control.add(tab_audio, text=_('Audio'))
        tab_control.pack(expand=True, fill=tk.BOTH)

        ttk.Label(tab_display, text=_('Screen resolution') + ' ').grid(
            row=0,
            column=0,
            padx=SPACE_BETWEEN,
            pady=SPACE_BETWEEN
        )

        ttk.Combobox(
            tab_display,
            values=supported_screen_resolutions(),
            textvariable=self.screen_resolution,
            state='readonly'
        ).grid(row=0, column=1, pady=SPACE_BETWEEN)

        ttk.Checkbutton(tab_display,
                        text=_('Fullscreen'),
                        variable=self.fullscreen,
                        onvalue=True,
                        offvalue=False,
                        command=self.on_toggle_fullscreen
                        ).grid(row=1, column=1, sticky='nw', pady=SPACE_BETWEEN)

        self.borderless_check = ttk.Checkbutton(
            tab_display,
            text=_('Borderless'),
            variable=self.borderless,
            onvalue=True,
            offvalue=False,
        )

        self.borderless_check.grid(row=2, column=1, pady=SPACE_BETWEEN, sticky='nw')

        self.on_toggle_fullscreen()

        ttk.Checkbutton(tab_display,
                        text=_('V-Sync'),
                        variable=self.vsync,
                        onvalue=True,
                        offvalue=False
                        ).grid(row=3, column=1, pady=SPACE_BETWEEN, sticky='nw')

        ttk.Label(tab_graphics, text=_('Antialiasing') + ' ').grid(
            row=0,
            column=0,
            padx=SPACE_BETWEEN,
            pady=SPACE_BETWEEN
        )

        ttk.Combobox(
            tab_graphics,
            values=list(self.antialiasing_dropdown_items().keys()),
            textvariable=self.antialiasing,
            state='readonly'
        ).grid(row=0, column=1, pady=SPACE_BETWEEN)

        ttk.Checkbutton(
            tab_graphics,
            text=_('Shaders'),
            variable=self.shaders,
            onvalue=True,
            offvalue=False,
        ).grid(row=1, column=1, pady=SPACE_BETWEEN, sticky='nw')

        ttk.Checkbutton(
            tab_graphics,
            text=_('Traffic'),
            variable=self.traffic,
            onvalue=True,
            offvalue=False
        ).grid(row=2, column=1, pady=SPACE_BETWEEN, sticky='nw')

        ttk.Checkbutton(
            tab_graphics,
            text=_('Animated Sky'),
            variable=self.sky,
            onvalue=True,
            offvalue=False
        ).grid(row=3, column=1, sticky='nw')

        videos_state = tk.NORMAL

        if not is_windows():
            videos_state = tk.DISABLED

        ttk.Checkbutton(
            tab_graphics,
            text=_('Videos'),
            variable=self.videos,
            onvalue=True,
            offvalue=False,
            state=videos_state
        ).grid(row=4, column=1, sticky='nw')

        ttk.Label(tab_audio, text=_('Audio Backend') + ' ').grid(
            row=0,
            column=0,
            padx=SPACE_BETWEEN,
            pady=SPACE_BETWEEN
        )

        ttk.Combobox(
            tab_audio,
            values=AUDIO_BACKENDS,
            textvariable=self.audio_backend,
            state='readonly'
        ).grid(row=0, column=2, pady=SPACE_BETWEEN, sticky='e')

        button_launch = ttk.Button(text=_('Launch Game'), command=self.on_launch)

        button_launch.pack(expand=True, fill=tk.BOTH, ipady=10)

        self.eval('tk::PlaceWindow . center')
        self.resizable(False, False)
        button_launch.focus_set()

    def bind_keyevents(self) -> None:
        """ Bind keyboard events"""

        # ESC key will quit the app
        self.bind('<Escape>', lambda e: self.destroy())

        # RETURN key will start the game
        self.bind('<Return>', self.on_launch)

    def set_icon(self) -> None:
        """
        Set window icon
        """
        icon = PhotoImage(file=os.path.join(self.path_state.ui_dir, 'icon.ico'))
        self.tk.call('wm', 'iconphoto', self._w, icon)

    def get_args(self):
        if not self.confirmed:
            return None

        # Apply settings in state
        self.state.fullscreen = self.fullscreen.get()
        self.state.borderless = self.borderless.get()
        self.state.vsync = self.vsync.get()
        self.state.antialiasing = self.text_to_selected_antialiasing(self.antialiasing.get())
        self.state.sky = self.sky.get()
        self.state.traffic = self.traffic.get()
        self.state.shaders = self.shaders.get()
        self.state.videos = self.videos.get()

        w, h = self.screen_resolution.get().split('x')
        self.state.screen_resolution = [w, h]
        self.state.audio_backend = self.audio_backend.get()
        self.state.first_start = True
        self.state.save()

        # Apply settings to args
        self.args.fullscreen = self.fullscreen.get()
        self.args.window = not self.fullscreen.get()
        self.args.borderless = self.borderless.get()
        self.args.no_vsync = not self.vsync.get()

        screen_resolution = self.screen_resolution.get().split('x')

        self.args.width = int(screen_resolution[0])
        self.args.height = int(screen_resolution[1])

        self.args.audio_backend = self.audio_backend.get()

        return self.args

    def on_launch(self, event=None):
        self.confirmed = True
        self.state.save()
        self.destroy()

    def on_toggle_fullscreen(self) -> None:
        """
        On toggle fullscreen enable or disable and uncheck the "Borderless" checkbox
        """
        if self.fullscreen.get():
            self.borderless_check.configure(state='disabled')
            self.borderless.set(False)
        else:
            self.borderless_check.configure(state='enabled')

    def autodetect_settings(self):
        screen_resolutions = supported_screen_resolutions()
        screen_resolutions = screen_resolutions[-1:]
        if len(screen_resolutions) >= 1:
            self.screen_resolution.set(screen_resolutions[0])

        logging.info(sys.argv)

        frozen = getattr(sys, "frozen", False)

        if frozen:
            logging.info(sys.argv)
            logging.info(sys.executable)
            shell([sys.argv[0], '--autodetect'])
        else:
            shell([sys.executable, sys.argv[0], '--autodetect'])

        settings = ''

        if get_autodetect_path():
            with open(get_autodetect_path(), 'r') as f:
                settings = f.read().strip()

        self.apply_preset(settings)

    def value_to_selected_antialiasing(self, value):
        items = self.antialiasing_dropdown_items()

        for key in items:
            if items[key] == value:
                return key

        return _('Off')

    def text_to_selected_antialiasing(self, key):
        items = self.antialiasing_dropdown_items()
        return items[key]

    def antialiasing_dropdown_items(self):

        return {
            _('Off'): 0,
            _('Low'): 2,
            _('Medium'): 4,
            _('High'): 8,
            _('Very High'): 16
        }
