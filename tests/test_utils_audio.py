import os
import unittest

import pygame

from utils.audio import play_sound, play_music, stop_music, get_devices


class AudioTest(unittest.TestCase):

    def setUp(self):
        pygame.mixer.init()

        self.test_file = os.path.join(os.path.dirname(__file__), 'test.ogg')
        self.test_sound = pygame.mixer.Sound(self.test_file)

    def tearDown(self):
        pygame.mixer.quit()

    def test_play_sound(self):
        sound = play_sound(self.test_file)
        self.assertTrue(sound.get_busy())
        sound.stop()

        self.assertFalse(sound.get_busy())

    def test_play_music(self):
        play_music(self.test_file, 2)
        self.assertTrue(pygame.mixer.music.get_busy())

        pygame.time.delay(2000)
        self.assertTrue(pygame.mixer.music.get_busy())

        pygame.time.delay(2000)
        self.assertFalse(pygame.mixer.music.get_busy())

    def test_play_music(self):
        play_music(self.test_file, 2)
        self.assertTrue(pygame.mixer.music.get_busy())
        stop_music()
        self.assertFalse(pygame.mixer.music.get_busy())

    def test_get_devices(self):
        self.assertGreaterEqual(len(get_devices()), 1)

        for device in get_devices():
            self.assertIs(str, type(device))
