import os

import arcade

from sprites.ui.inventoryitem import InventoryItem

CAPACITY = 5

MARGIN = 10
LEFT = MARGIN
BOTTOM = MARGIN
SPACE_BETWEEN = 10


class InventoryContainer(arcade.sprite_list.SpriteList):
    def __init__(self):
        super().__init__(capacity=CAPACITY, visible=True)

        self.visible = True

    def setup(self, state, size):
        self.clear()
        file = os.path.join(state.image_dir, 'ui', 'inventory.png')

        bottom = BOTTOM
        left = LEFT

        total_width = 0

        for i in range(CAPACITY):
            sprite = InventoryItem(filename=file, bottom=bottom, left=left)
            sprite.setup(state=state)
            self.append(sprite)

            left += sprite.width + SPACE_BETWEEN
            total_width += sprite.width + SPACE_BETWEEN

        w, h = size
        w = w / 2

        w -= total_width / 2

        left = w

        for sprite in self.sprite_list:
            sprite.left = left

            left += sprite.width + SPACE_BETWEEN

    def select(self, index):
        for sprite in self.sprite_list:
            sprite.unselect()

        if index < 0:
            return None

        self.sprite_list[index].select()

        return self.sprite_list[index].item

    def add_item(self, item):
        for sprite in self.sprite_list:
            if not sprite.get_item():
                sprite.set_item(item)
                return

            klass1 = sprite.item.__class__
            klass2 = item.__class__

            if klass1 != klass2:
                continue

            sprite.push()
            return

    def get_selected(self):
        for item in self.sprite_list:
            if item.selected:
                return item

        return None

    def get_item(self, index):
        return self.sprite_list[index]

    def next(self):
        index = 0
        selected = -1
        for item in self.sprite_list:
            if item.selected:
                selected = index
                break
            index += 1

        next_selected = selected + 1

        if (next_selected >= len(self.sprite_list)):
            next_selected = -1

        self.select(next_selected)

        return next_selected

    def previous(self):
        index = 0
        selected = -1
        for item in self.sprite_list:
            if item.selected:
                selected = index
                break
            index += 1

        next_selected = selected - 1

        if next_selected < -1:
            next_selected = len(self.sprite_list) - 1

        self.select(next_selected)

        return next_selected