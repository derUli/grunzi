import glob
import os
import tkinter as tk
import tkinter.ttk as ttk

import pyglet
from PIL.ImageTk import PhotoImage
from ttkthemes import ThemedTk

from state.settingsstate import SettingsState
from utils.utils import natural_keys

class LauncherWindow(ThemedTk):
    def __init__(self, theme='breeze', args=None, state=None):
        super().__init__(theme=theme)
        self.path_state = state
        self.args = args

        self.fullscreen = tk.BooleanVar(value=args.fullscreen)
        self.screen_resolution = tk.StringVar(
            value=str(args.width) + 'x' + str(args.height)
        )

        self.vsync = tk.BooleanVar(value=not args.no_vsync)
        self.silent = tk.BooleanVar(value=args.silent)
        self.controller = tk.BooleanVar(value=args.controller)
        self.map = tk.StringVar(value=args.map)

        self.state = SettingsState()
        self.confirmed = False

    def setup(self):
        self.title(_('Grunzi Launcher'))
        self.geometry('320x240')
        self.bind_keyevents()
        self.set_icon()

        if SettingsState.exists():
            self.state = SettingsState.load()
            self.fullscreen.set(self.state.fullscreen)
            self.vsync.set(self.state.vsync)
            self.silent.set(self.state.silent)
            self.controller.set(self.state.controller)
            w, h = self.state.screen_resolution[0], self.state.screen_resolution[1]
            self.screen_resolution.set(
                value=str(w) + 'x' + str(h)
            )

        tabControl = ttk.Notebook(self)

        tab_video = ttk.Frame(tabControl)
        tab_audio = ttk.Frame(tabControl)
        tab_controller = ttk.Frame(tabControl)
        tab_game = ttk.Frame(tabControl)

        tabControl.add(tab_video, text=_('Video'))
        tabControl.add(tab_audio, text=_('Audio'))
        tabControl.add(tab_controller, text=_('Controller'))
        tabControl.add(tab_game, text=_('Game'))
        tabControl.pack(expand=True, fill=tk.BOTH)

        label_text = tk.StringVar()
        label_text.set(_('Screen resolution:'))
        tk.Label(tab_video, textvariable=label_text).pack()

        ttk.Combobox(
            tab_video,
            values=self.supported_screen_resolutions(),
            textvariable=self.screen_resolution,
            state='readonly'
        ).pack()

        tk.Checkbutton(tab_video,
                       text=_('Fullscreen'),
                       variable=self.fullscreen,
                       onvalue=True,
                       offvalue=False
                       ).pack()

        tk.Checkbutton(tab_video,
                       text=_('V-Sync'),
                       variable=self.vsync,
                       onvalue=True,
                       offvalue=False
                       ).pack()

        tk.Checkbutton(
            tab_audio,
            text=_('Sound'),
            variable=self.silent,
            onvalue=False,
            offvalue=True
        ).pack()

        tk.Checkbutton(
            tab_controller,
            text=_('Use Controller'),
            variable=self.controller,
            onvalue=True,
            offvalue=False,
        ).pack()

        label_text = tk.StringVar()
        label_text.set(_('Map:'))
        tk.Label(tab_game, textvariable=label_text).pack()

        maps = self.available_maps()

        ttk.Combobox(
            tab_game,
            values=maps,
            textvariable=self.map,
            state='readonly'
        ).pack()

        button_launch = tk.Button(text=_('Launch Game'), command=self.on_launch)

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
        self.state.controller = self.controller.get()
        w, h = self.screen_resolution.get().split('x')
        self.state.screen_resolution = [w, h]
        self.state.save()

        # Apply settings to args
        self.args.fullscreen = self.fullscreen.get()
        self.args.window = not self.fullscreen.get()
        self.args.no_vsync = not self.vsync.get()

        self.args.silent = self.silent.get()
        self.args.controller = self.controller.get()
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
