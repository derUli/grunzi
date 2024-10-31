class AnimationConfig:
    def __init__(self, size, loop, frame_length, apply_modifier, reverse=False):
        self.size = size
        self.loop = loop
        self.frame_length = frame_length
        self.apply_modifier = apply_modifier
        self.reverse = reverse
