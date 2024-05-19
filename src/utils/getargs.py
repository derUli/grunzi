from state.argscontainer import ArgsContainer
from utils.callbackhandler import CallbackHandler
from views.view import View


def get_args(klaas: View):
    return ArgsContainer(
        player=klaas.player_sprite,
        scene=klaas.scene,
        physics_engine=klaas.physics_engine,
        state=klaas.state,
        map_size=klaas.tilemap.size,
        astar_barrier_list=klaas.astar_barrier_list,
        wall_spritelist=klaas.wall_spritelist,
        callbacks=CallbackHandler(on_complete=klaas.on_next_level)
    )