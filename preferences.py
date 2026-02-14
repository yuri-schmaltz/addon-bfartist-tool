import bpy

class BFA_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    enable_menu_entries: bpy.props.BoolProperty(
        name="Enable Menu Entries",
        description="Add entries to standard Blender menus (View, Mesh, etc.)",
        default=True
    )

    enable_header_button: bpy.props.BoolProperty(
        name="Enable Header Button",
        description="Add Reset View button to 3D View Header",
        default=False
    )

    enable_keymaps: bpy.props.BoolProperty(
        name="Enable Keymaps",
        description="Enable custom keymaps (e.g. Ctrl+Delete for Smart Delete)",
        default=True,
        update=lambda self, context: update_keymaps(self, context)
    )

    enable_shelf_header: bpy.props.BoolProperty(
        name="Enable Quick Shelf in Header",
        description="Add Quick Create popover to 3D View Header",
        default=True
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "enable_menu_entries")
        layout.prop(self, "enable_header_button")
        layout.prop(self, "enable_keymaps")
        layout.prop(self, "enable_shelf_header")


def update_keymaps(self, context):
    from . import keymap
    if self.enable_keymaps:
        keymap.register_keymaps()
    else:
        keymap.unregister_keymaps()

def register():
    bpy.utils.register_class(BFA_AddonPreferences)

def unregister():
    bpy.utils.unregister_class(BFA_AddonPreferences)
