import os
class ViewState:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.data_dir = os.path.join(root_dir, 'data')
        self.map_dir = os.path.join(self.data_dir, 'levels')
        self.image_dir = os.path.join(self.data_dir, 'images')
        self.sprite_dir = os.path.join(self.image_dir, 'sprites')
        self.music_dir = os.path.join(self.data_dir, 'music')