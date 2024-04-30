import os
import tkinter as tk
import tkinter.ttk as ttk

import pyglet.canvas
from PIL.ImageTk import PhotoImage
from ttkthemes import ThemedTk

from constants.audio import AUDIO_BACKENDS
from state.settingsstate import SettingsState
from utils.screen import supported_screen_resolutions

NOTEBOOK_PADDING = 20

SPACE_BETWEEN = 5

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

        self.audio_backend = tk.StringVar(value=args.audio_backend)
        self.state = SettingsState()
        self.confirmed = False
        self.borderless_check = None

    def setup(self) -> None:
        """
        Set up the UI
        """
        self.title(_('Grunzi Launcher'))
        self.geometry('320x240')
        self.bind_keyevents()
        self.set_icon()

        if SettingsState.exists():
            self.state = SettingsState.load()

            self.fullscreen.set(self.state.fullscreen)
            self.vsync.set(self.state.vsync)
            self.borderless.set(self.state.borderless)
            w, h = self.state.screen_resolution[0], self.state.screen_resolution[1]
            self.screen_resolution.set(
                value=str(w) + 'x' + str(h)
            )

            self.audio_backend.set(self.state.audio_backend)

        tab_control = ttk.Notebook(self)

        tab_video = ttk.Frame(tab_control, padding=NOTEBOOK_PADDING)
        tab_audio = ttk.Frame(tab_control, padding=NOTEBOOK_PADDING)

        tab_control.add(tab_video, text=_('Video'))
        tab_control.add(tab_audio, text=_('Audio'))
        tab_control.pack(expand=True, fill=tk.BOTH)

        ttk.Label(tab_video, text=_('Screen resolution:')).pack(expand=True)

        ttk.Combobox(
            tab_video,
            values=supported_screen_resolutions(),
            textvariable=self.screen_resolution,
            state='readonly'
        ).pack(expand=True)

        ttk.Checkbutton(tab_video,
                        text=_('Fullscreen'),
                        variable=self.fullscreen,
                        onvalue=True,
                        offvalue=False,
                        command=self.on_toggle_fullscreen
                        ).pack(expand=True)

        self.borderless_check = ttk.Checkbutton(tab_video,
                                                text=_('Borderless'),
                                                variable=self.borderless,
                                                onvalue=True,
                                                offvalue=False,
                                                )

        self.borderless_check.pack(expand=True)

        self.on_toggle_fullscreen()

        ttk.Checkbutton(tab_video,
                        text=_('V-Sync'),
                        variable=self.vsync,
                        onvalue=True,
                        offvalue=False
                        ).pack(expand=True)

        ttk.Label(tab_audio, text=_('Audio Backend:')).pack()

        ttk.Combobox(
            tab_audio,
            values=AUDIO_BACKENDS,
            textvariable=self.audio_backend,
            state='readonly'
        ).pack()

        button_launch = ttk.Button(text=_('Launch Game'), command=self.on_launch)

        button_launch.pack(expand=True, fill=tk.BOTH)

        self.resizable(False, False)
        button_launch.focus_set()

    def bind_keyevents(self):
        """ Bind keyboard events"""

        # ESC key will quit the app
        self.bind('<Escape>', lambda e: self.destroy())

        # RETURN key will start the game
        self.bind('<Return>', self.on_launch)

    def set_icon(self) -> None:
        """
        Set window icon
        """
        icon = PhotoImage(file=os.path.join(self.path_state.image_dir, 'ui', 'icon.ico'))
        self.tk.call('wm', 'iconphoto', self._w, icon)

    def get_args(self):
        if not self.confirmed:
            return None

        # Apply settings in state
        self.state.fullscreen = self.fullscreen.get()
        self.state.borderless = self.borderless.get()
        self.state.vsync = self.vsync.get()

        w, h = self.screen_resolution.get().split('x')
        self.state.screen_resolution = [w, h]
        self.state.audio_backend = self.audio_backend.get()
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
