import glob
import os
import tkinter as tk
import tkinter.ttk as ttk

import pyglet
from PIL.ImageTk import PhotoImage

from state.settingsstate import SettingsState
from utils.utils import natural_keys


class LauncherWindow(tk.Tk):
    def __init__(self, args, state):
        super().__init__()
        self.path_state = state
        self.args = args

        self.fullscreen = tk.BooleanVar(value=args.fullscreen)
        self.screen_resolution = tk.StringVar(
            value=str(args.width) + 'x' + str(args.height)
        )
        self.silent = tk.BooleanVar(value=args.silent)
        self.controller = tk.BooleanVar(value=args.controller)
        self.debug = tk.BooleanVar(value=args.debug)
        self.map = tk.StringVar(value=args.map)

        self.state = SettingsState()
        self.confirmed = False

    def setup(self):
        self.withdraw()
        self.title(_('Grunzi Launcher'))
        self.geometry('320x240')

        self.bind_keyevents()
        self.set_icon()

        if SettingsState.exists():
            self.state = SettingsState.load()
            self.fullscreen.set(self.state.fullscreen)
            self.silent.set(self.state.silent)
            self.controller.set(self.state.controller)
            self.debug.set(self.state.debug)
            w, h = self.state.screen_resolution[0], self.state.screen_resolution[1]
            self.screen_resolution.set(
                value=str(w) + 'x' + str(h)
            )

        checkbox_fullscreen = tk.Checkbutton(
            text=_('Fullscreen'),
            variable=self.fullscreen,
            onvalue=True,
            offvalue=False
        )
        checkbox_fullscreen.pack()

        checkbox_sound = tk.Checkbutton(
            text=_('Sound'),
            variable=self.silent,
            onvalue=False,
            offvalue=True
        )
        checkbox_sound.pack()

        checkbox_controller = tk.Checkbutton(
            text=_('Use Controller'),
            variable=self.controller,
            onvalue=True,
            offvalue=False
        )
        checkbox_controller.pack()

        checkbox_debug = tk.Checkbutton(
            text=_('Debug'),
            variable=self.debug,
            onvalue=True,
            offvalue=False
        )
        checkbox_debug.pack()

        label_text = tk.StringVar()
        label_text.set(_('Screen resolution:'))
        label = tk.Label(self, textvariable=label_text)
        label.pack()

        modes = self.supported_screen_resolutions()

        screen_resolution = ttk.Combobox(
            values=modes,
            textvariable=self.screen_resolution,
            state='readonly'
        )
        screen_resolution.pack()

        label_text = tk.StringVar()
        label_text.set(_('Map:'))
        label = tk.Label(self, textvariable=label_text)
        label.pack()

        maps = self.available_maps()

        maps = ttk.Combobox(
            values=maps,
            textvariable=self.map,
            state='readonly'
        )
        maps.pack()

        button_launch = tk.Button(text=_('Launch Game'), command=self.on_launch)
        button_launch.pack(expand=True)

        self.resizable(False, False)

        self.deiconify()

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
        self.state.silent = self.silent.get()
        self.state.controller = self.controller.get()
        self.state.debug = self.debug.get()
        w, h = self.screen_resolution.get().split('x')
        self.state.screen_resolution = [w, h]
        self.state.save()

        # Apply settings to args
        self.args.fullscreen = self.fullscreen.get()
        self.args.window = not self.fullscreen.get()
        self.args.silent = self.silent.get()
        self.args.controller = self.controller.get()
        self.args.debug = self.debug.get()

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
