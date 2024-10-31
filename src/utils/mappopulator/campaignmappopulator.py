import time

from state.argscontainer import ArgsContainer
from utils.mappopulator.mappopulator import MapPopulator


class CampaignMapPopulator(MapPopulator):

    def spawn_initial(self, args: ArgsContainer) -> None:
        """ Spawn some sprites on level load """

        self.init_npc_spritelist(args)

        if not self.enabled:
            return

        self.schedule_landmine(args)
        self.schedule_food(args)
        self.schedule_snow(args)
        self.schedule_hell_particles(args)

    def update(self, args: ArgsContainer) -> None:
        """ Update map campaignmappopulator """

        if not self.enabled:
            return

        # These are only initialized when the game starts
        if not self.initialized:
            self.spawn_next_initial(0, args)

        if time.time() < self.next_spawn:
            return

        from constants.layers import LAYER_NPC
        from sprites.characters.character import Character

        try:
            enemies = args.scene[LAYER_NPC]

        except KeyError:
            enemies = []

        enemies = list(filter(lambda x: isinstance(x, Character), enemies))

        # There is a maximum NPC count
        if len(enemies) >= args.state.difficulty.max_npcs:
            return

        self.spawn(args)
