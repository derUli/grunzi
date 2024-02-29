#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk

from state.settingsstate import SettingsState


class LauncherWindow(tk.Tk):
    def __init__(self, args):
        super().__init__()

        self.title(_('Grunzi Launcher'))
        self.geometry('320x320')

        self.fullscreen = tk.BooleanVar(value=args.fullscreen)
        self.screen_resolution = tk.StringVar(
            value=str(args.width) + 'x' + str(args.height)
        )
        self.silent = tk.BooleanVar(value=args.silent)
        self.state = SettingsState()

        if SettingsState.exists():
            self.state = SettingsState.load()
            self.fullscreen.set(self.state.fullscreen)
            self.silent.set(self.state.silent)
            w, h = self.state.screen_resolution[0], self.state.screen_resolution[1]
            self.screen_resolution.set(
                value=str(w) + 'x' + str(h)
            )

        self.args = args

        self.confirmed = False

    def setup(self):
        checkbox_fullscreen = tk.Checkbutton(
            text=_('Fullscreen'),
            variable=self.fullscreen,
            onvalue=True,
            offvalue=False
        )
        checkbox_fullscreen.pack()

        checkbox_silent = tk.Checkbutton(
            text=_('Silent'),
            variable=self.silent,
            onvalue=True,
            offvalue=False
        )
        checkbox_silent.pack()

        label_text = tk.StringVar()
        label_text.set(_('Screen resolution:'))
        label = tk.Label(self, textvariable=label_text)
        label.pack()

        screen_resolution = ttk.Combobox(
            values=[
                "1280x720",
                "1366x768",
                "1600x900",
                "1920x1080",
                "2560x1440",
                "3840x2160",
                "7680x4320"
            ],
            textvariable=self.screen_resolution,
            state='readonly'
        )
        screen_resolution.pack()

        button_launch = tk.Button(text=_('Launch Game'), command=self.on_launch)
        button_launch.pack(expand=True)

        self.resizable(False, False)

    def get_args(self):
        if not self.confirmed:
            return None

        self.state.fullscreen = self.fullscreen.get()
        self.state.silent = self.silent.get()

        w, h = self.screen_resolution.get().split('x')
        self.state.screen_resolution = [w, h]
        self.state.save()

        self.args.fullscreen = self.fullscreen.get()
        self.args.window = not self.fullscreen.get()
        self.args.silent = self.silent.get()

        screen_resolution = self.screen_resolution.get().split('x')

        self.args.width = int(screen_resolution[0])
        self.args.height = int(screen_resolution[1])

        return self.args

    def on_launch(self):
        self.confirmed = True
        self.state.save()
        self.destroy()
