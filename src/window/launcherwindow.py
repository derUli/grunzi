import argparse
import logging
import os
import tkinter as tk
import tkinter.ttk as ttk

from PIL.ImageTk import PhotoImage
from ttkthemes import ThemedTk

from constants.audio import audio_backends
from state.settingsstate import SettingsState
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

        quality = args.video_quality
        if quality is None:
            quality = 4

        self.quality = tk.IntVar(value=quality)

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
            self.quality.set(self.state.quality)

            w, h = self.state.screen_resolution[0], self.state.screen_resolution[1]
            self.screen_resolution.set(
                value=str(w) + 'x' + str(h)
            )

            self.audio_backend.set(self.state.audio_backend)

        # Detect screen resolution on first start
        if not self.state.first_start:
            self.screen_resolution.set(supported_screen_resolutions()[-1])

        tab_control = ttk.Notebook(self)

        tab_graphics = ttk.Frame(tab_control, padding=NOTEBOOK_PADDING)
        tab_audio = ttk.Frame(tab_control, padding=NOTEBOOK_PADDING)

        tab_control.add(tab_graphics, text=_('Graphics'))
        tab_control.add(tab_audio, text=_('Audio'))
        tab_control.pack(expand=True, fill=tk.BOTH)

        ttk.Label(tab_graphics, text=_('Screen resolution') + ' ').grid(
            row=0,
            column=0,
            padx=SPACE_BETWEEN,
            pady=SPACE_BETWEEN
        )

        ttk.Combobox(
            tab_graphics,
            values=supported_screen_resolutions(),
            textvariable=self.screen_resolution,
            state='readonly'
        ).grid(row=0, column=1, pady=SPACE_BETWEEN)

        ttk.Checkbutton(
            tab_graphics,
            text=_('Fullscreen'),
            variable=self.fullscreen,
            onvalue=True,
            offvalue=False,
            command=self.on_toggle_fullscreen
        ).grid(row=1, column=1, sticky='nw', pady=SPACE_BETWEEN)

        self.borderless_check = ttk.Checkbutton(
            tab_graphics,
            text=_('Borderless'),
            variable=self.borderless,
            onvalue=True,
            offvalue=False,
        )

        self.borderless_check.grid(row=2, column=1, pady=SPACE_BETWEEN, sticky='nw')

        self.on_toggle_fullscreen()

        ttk.Checkbutton(tab_graphics,
                        text=_('V-Sync'),
                        variable=self.vsync,
                        onvalue=True,
                        offvalue=False
                        ).grid(row=3, column=1, pady=SPACE_BETWEEN, sticky='nw')

        ttk.Label(tab_graphics, text=_('Quality') + ' ').grid(
            row=4,
            column=0,
            padx=SPACE_BETWEEN,
            pady=SPACE_BETWEEN
        )

        (ttk.Scale(tab_graphics, from_=0, to=6, variable=self.quality,tickinterval=1).
         grid(row=4, column=1, pady=SPACE_BETWEEN, sticky='nw'))

        ttk.Label(tab_audio, text=_('Audio Backend') + ' ').grid(
            row=0,
            column=0,
            padx=SPACE_BETWEEN,
            pady=SPACE_BETWEEN
        )

        ttk.Combobox(
            tab_audio,
            values=audio_backends(),
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

    def get_args(self) -> argparse.Namespace | None:
        """
        Apply selected settings to args
        @return: Argparse Namespace
        """

        if not self.confirmed:
            return None

        # Apply settings in state
        self.state.fullscreen = self.fullscreen.get()
        self.state.borderless = self.borderless.get()
        self.state.vsync = self.vsync.get()

        if self.state.quality != self.quality.get():
            self.state.quality = self.quality.get()
            self.args.video_quality = self.quality.get()

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
        logging.debug(event)

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
