class ArgsContainer:
    def __init__(
            self,
            player=None,
            scene=None,
            physics_engine=None,
            state=None,
            map_size=None,
            astar_barrier_list=None,
            wall_spritelist=None
    ):
        self.player = player
        self.scene = scene
        self.physics_engine = physics_engine
        self.state = state
        self.map_size = map_size
        self.astar_barrier_list = astar_barrier_list
        self.wall_spritelist
