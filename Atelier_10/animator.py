import random
from maya import cmds

GROUP_NAME = "scatter_grp"


def get_selected_object():
    """Retourne le premier objet sélectionné, ou None s'il n'y en a pas."""
    selection = cmds.ls(selection=True, transforms=True)
    if not selection:
        return None
    return selection[0]


def scatter(source, count, radius, seed):
    """Duplique 'source' (count fois) au hasard autour de lui.

    source : nom de l'objet à propager (le cactus)
    count  : nombre de copies
    radius : distance maximale en X et en Z
    seed   : graine du hasard (même seed = mêmes positions)
    """
    # Tout le scatter devient UNE seule action dans l'historique (un Ctrl+Z)
    cmds.undoInfo(openChunk=True)
    try:
        # On supprime l'ancien groupe, sinon les copies s'accumulent
        if cmds.objExists(GROUP_NAME):
            cmds.delete(GROUP_NAME)

        random.seed(seed)
        group = cmds.group(empty=True, name=GROUP_NAME)

        for _ in range(count):
            copy = cmds.duplicate(source)[0]
            copy = cmds.parent(copy, group)[0]
            x = random.uniform(-radius, radius)
            z = random.uniform(-radius, radius)
            cmds.move(x, 0, z, copy, relative=True)
    finally:
        cmds.undoInfo(closeChunk=True)

    # group et parent changent la sélection : on remet l'objet d'origine
    cmds.select(source)