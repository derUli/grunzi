""" Args Container """
from utils.callbackhandler import CallbackHandler


class ArgsContainer:
    """ This class is used as an argument container for the """

    def __init__(
            self,
            player=None,
            scene=None,
            physics_engine=None,
            state=None,
            map_size=None,
            astar_barrier_list=None,
            wall_spritelist=None,
            callbacks=None,
            camera_gui=None,
            camera=None,
            tilemap=None,
            inventory=None,
            controllers=None,
            music_queue = None
    ):
        """
        Constructor
        @param player:
        @param scene:
        @param physics_engine:
        @param state:
        @param map_size:
        @param astar_barrier_list:
        @param wall_spritelist:
        @param callbacks:
        @param camera_gui:
        @param camera:
        @param tilemap:
        @param inventory:
        @param controllers:
        """

        if controllers is None:
            controllers = []

        self.player = player
        self.scene = scene
        self.physics_engine = physics_engine
        self.state = state
        self.map_size = map_size
        self.astar_barrier_list = astar_barrier_list
        self.wall_spritelist = wall_spritelist
        self.callbacks = callbacks
        self.camera = camera
        self.camera_gui = camera_gui
        self.tilemap = tilemap
        self.inventory = inventory
        self.controllers = controllers
        self.music_queue = music_queue


def make_args_container(klaas) -> ArgsContainer:
    """
    Make ArgsContainer
    @param klaas: Game class
    @return: The args container
    """

    return ArgsContainer(
        player=klaas.scene.player_sprite,
        scene=klaas.scene,
        physics_engine=klaas.physics_engine,
        state=klaas.state,
        map_size=klaas.tilemap.size,
        astar_barrier_list=klaas.astar_barrier_list,
        wall_spritelist=klaas.wall_spritelist,
        callbacks=CallbackHandler(on_complete=klaas.on_next_level),
        camera=klaas.camera_sprites,
        camera_gui=klaas.camera_gui,
        tilemap=klaas.tilemap,
        inventory=klaas.ui.inventory,
        controllers=klaas.window.controllers,
        music_queue=klaas.music_queue
    )
