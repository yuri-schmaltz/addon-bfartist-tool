import bpy

addon_keymaps = []

def register_keymaps():
    wm = bpy.context.window_manager
    if not wm.keyconfigs.addon:
        return

    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    
    # Smart Delete: Ctrl+Delete
    kmi = km.keymap_items.new("bfa.smart_delete", 'DEL', 'PRESS', ctrl=True)
    
    addon_keymaps.append((km, kmi))

def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
