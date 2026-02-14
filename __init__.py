bl_info = {
    "name": "BFA Tools for Blender",
    "author": "Yuri Schmaltz / BFA Team",
    "version": (0, 1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > BFA Tools",
    "description": "Port of Bforartists usability tools to official Blender",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

import bpy
from . import preferences
from . import operators
from . import ui
from . import keymap

modules = (
    preferences,
    operators,
    ui,
)

def register():
    for mod in modules:
        mod.register()
        
    # Register keymaps if enabled
    prefs = bpy.context.preferences.addons[__package__].preferences
    if prefs.enable_keymaps:
        keymap.register_keymaps()

def unregister():
    keymap.unregister_keymaps()
    
    for mod in reversed(modules):
        mod.unregister()

if __name__ == "__main__":
    register()
