'''
This is a quick example of integrating a video into a pyglet project
Double buffering is turned off to benefit from turning off force draw on the video
'''


import pyglet 
from pyvidplayer2 import VideoPyglet

video = VideoPyglet(r"intro.webm")
video.resize((1280, 720))

def update(dt):
    video.draw((0, 0), force_draw=True)

    print(video.active)

win = pyglet.window.Window(width=1280, height=720, config=pyglet.gl.Config(double_buffer=True), caption=f"pyglet support demo")

pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()
video.close()