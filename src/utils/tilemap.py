""" Tilemap """

import arcade

from utils.sprite import tilemap_size


class TileMap:
    """ Tilemap class """

    def __init__(
            self,
            filename,
            layer_options,
            use_spatial_hash=True,
            hit_box_algorithm="Simple",
            hit_box_detail=4.5,
            lazy=True
    ):
        """
        Constructor
        @param filename: filename
        @param layer_options: layer options
        @param use_spatial_hash: use spatial hash
        @param hit_box_algorithm: hit box algorithm
        """
        self._map = arcade.load_tilemap(
            filename,
            layer_options=layer_options,
            use_spatial_hash=use_spatial_hash,
            hit_box_algorithm=hit_box_algorithm,
            hit_box_detail=hit_box_detail,
            lazy=lazy
        )

        self._size = tilemap_size(self._map)
        self._width, self._height = self._size

    @property
    def map(self) -> arcade.tilemap.TileMap:
        """
        Tilemap
        @return: TileMap
        """
        return self._map

    @property
    def size(self) -> tuple:
        """ Tilemap size
        @return: size tuple
        """
        return self._size

    @property
    def width(self) -> int:
        """ Tilemap width
        @return: width int
        """
        return self._width

    @property
    def height(self) -> int:
        """ Tilemap height
        @return: height int
        """
        return self._height
