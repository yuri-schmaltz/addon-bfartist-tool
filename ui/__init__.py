from . import panels
from . import menus
from . import shelf

modules = (
    panels,
    menus,
    shelf,
)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
