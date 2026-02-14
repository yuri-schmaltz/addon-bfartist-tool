from . import view
from . import mesh
from . import materials

modules = (
    view,
    mesh,
    materials,
)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
