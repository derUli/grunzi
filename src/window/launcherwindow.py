import glob
import logging
import os
import tkinter as tk
import tkinter.ttk as ttk

import pyglet
from PIL.ImageTk import PhotoImage
from ttkthemes import ThemedTk

from state.settingsstate import SettingsState
from utils.utils import natural_keys

NOTEBOOK_PADDING = 20

SPACE_BETWEEN = 5


class LauncherWindow(ThemedTk):
    def __init__(self, theme='equilux', args=None, state=None):
        super().__init__(theme=theme)

        self.path_state = state
        self.args = args

        self.fullscreen = tk.BooleanVar(value=args.fullscreen)
        self.screen_resolution = tk.StringVar(
            value=str(args.width) + 'x' + str(args.height)
        )

        self.vsync = tk.BooleanVar(value=not args.no_vsync)
        self.silent = tk.BooleanVar(value=args.silent)

        self.map = tk.StringVar(value=args.map)

        self.state = SettingsState()
        self.confirmed = False

    def setup(self):
        self.title(_('Grunzi Launcher'))
        self.geometry('320x240')
        self.bind_keyevents()
        self.set_icon()

        if SettingsState.exists():
            self.state = SettingsState()

            try:
                self.state = SettingsState.load()
            except ValueError as e:
                logging.error(e)
            except OSError as e:
                logging.error(e)
            except AttributeError as e:
                logging.error(e)

            self.fullscreen.set(self.state.fullscreen)
            self.vsync.set(self.state.vsync)
            self.silent.set(self.state.silent)
            w, h = self.state.screen_resolution[0], self.state.screen_resolution[1]
            self.screen_resolution.set(
                value=str(w) + 'x' + str(h)
            )

        tabControl = ttk.Notebook(self)

        tab_video = ttk.Frame(tabControl, padding=NOTEBOOK_PADDING)
        tab_audio = ttk.Frame(tabControl, padding=NOTEBOOK_PADDING)
        tab_game = ttk.Frame(tabControl, padding=NOTEBOOK_PADDING)

        tabControl.add(tab_video, text=_('Video'))
        tabControl.add(tab_audio, text=_('Audio'))
        tabControl.add(tab_game, text=_('Game'))
        tabControl.pack(expand=True, fill=tk.BOTH)

        ttk.Label(tab_video, text=_('Screen resolution:')).pack(expand=True)

        ttk.Combobox(
            tab_video,
            values=self.supported_screen_resolutions(),
            textvariable=self.screen_resolution,
            state='readonly'
        ).pack(expand=True)

        ttk.Checkbutton(tab_video,
                        text=_('Fullscreen'),
                        variable=self.fullscreen,
                        onvalue=True,
                        offvalue=False
                        ).pack(expand=True)

        ttk.Checkbutton(tab_video,
                        text=_('V-Sync'),
                        variable=self.vsync,
                        onvalue=True,
                        offvalue=False
                        ).pack(expand=True)

        ttk.Checkbutton(
            tab_audio,
            text=_('Sound'),
            variable=self.silent,
            onvalue=False,
            offvalue=True
        ).pack()

        ttk.Label(tab_game, text=_('Map:')).pack()

        maps = self.available_maps()

        ttk.Combobox(
            tab_game,
            values=maps,
            textvariable=self.map,
            state='readonly'
        ).pack()

        button_launch = ttk.Button(text=_('Launch Game'), command=self.on_launch)

        button_launch.pack(expand=True, fill=tk.BOTH)

        self.resizable(False, False)
        button_launch.focus_set()

    def bind_keyevents(self):
        self.bind('<Escape>', lambda e: self.destroy())
        self.bind('<Return>', self.on_launch)

    def set_icon(self):
        icon = PhotoImage(file=os.path.join(self.path_state.image_dir, 'ui', 'icon.ico'))
        self.tk.call('wm', 'iconphoto', self._w, icon)

    def get_args(self):
        if not self.confirmed:
            return None

        # Apply settings in state
        self.state.fullscreen = self.fullscreen.get()
        self.state.vsync = self.vsync.get()
        self.state.silent = self.silent.get()
        w, h = self.screen_resolution.get().split('x')
        self.state.screen_resolution = [w, h]
        self.state.save()

        # Apply settings to args
        self.args.fullscreen = self.fullscreen.get()
        self.args.window = not self.fullscreen.get()
        self.args.no_vsync = not self.vsync.get()

        self.args.silent = self.silent.get()
        self.args.map = self.map.get()

        screen_resolution = self.screen_resolution.get().split('x')

        self.args.width = int(screen_resolution[0])
        self.args.height = int(screen_resolution[1])

        return self.args

    def on_launch(self, event=None):
        self.confirmed = True
        self.state.save()
        self.destroy()

    def supported_screen_resolutions(self):
        modes = pyglet.canvas.get_display().get_default_screen().get_modes()

        mode_values = []

        for mode in modes:
            item = str(mode.width) + "x" + str(mode.height)
            if item not in mode_values:
                mode_values.append(item)

        return sorted(mode_values, key=natural_keys)

    def available_maps(self):
        maps = []
        dir = os.path.join(self.path_state.map_dir, '*.tmx')
        for file in glob.glob(dir):
            maps.append(
                os.path.splitext(
                    os.path.basename(file)
                )[0]
            )

        return sorted(maps, key=natural_keys)
