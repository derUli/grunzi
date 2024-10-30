import time

from state.argscontainer import ArgsContainer
from utils.mappopulator.mappopulator import MapPopulator


class CampaignMapPopulator(MapPopulator):

    def spawn_initial(self, args: ArgsContainer) -> None:
        """ Spawn some sprites on level load """

        self.init_npc_spritelist(args)

        if not self.enabled:
            return

        self.spawn_food(args)
        self.spawn_landmine(args)
        self.spawn_snow(args)
        self.schedule_hell_particles(args)

    def update(self, args: ArgsContainer) -> None:
        if not self.enabled:
            return

        if not self.initialized:
            self.initialized = time.time()
            self.spawn_next_initial(0, args)

        if time.time() < self.next_spawn:
            return

        from constants.layers import LAYER_NPC

        try:
            enemies = args.scene[LAYER_NPC]
        except KeyError:
            enemies = []

        if len(enemies) >= args.state.difficulty.max_npcs:
            return

        self.spawn(args)
