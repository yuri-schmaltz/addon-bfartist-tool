import bpy

class BFA_PT_shelf(bpy.types.Panel):
    """BFA Quick Shelf Panel in Sidebar"""
    bl_label = "Quick Create"
    bl_category = "BFA Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    # bl_parent_id = "VIEW3D_PT_bfa_tools" # Optional: make it sub-panel
    
    def draw(self, context):
        layout = self.layout
        draw_shelf(layout)

def draw_shelf(layout):
    """Draws the shelf content (icons)"""
    
    # Primitives
    layout.label(text="Primitives")
    row = layout.row(align=True)
    row.operator("mesh.primitive_cube_add", text="", icon='MESH_CUBE')
    row.operator("mesh.primitive_uv_sphere_add", text="", icon='MESH_UVSPHERE')
    row.operator("mesh.primitive_cylinder_add", text="", icon='MESH_CYLINDER')
    row.operator("mesh.primitive_plane_add", text="", icon='MESH_PLANE')
    row.operator("mesh.primitive_torus_add", text="", icon='MESH_TORUS')
    row.operator("mesh.primitive_monkey_add", text="", icon='MESH_MONKEY')
    
    # Lights
    layout.label(text="Lights")
    row = layout.row(align=True)
    row.operator("object.light_add", text="", icon='LIGHT_POINT').type='POINT'
    row.operator("object.light_add", text="", icon='LIGHT_SUN').type='SUN'
    row.operator("object.light_add", text="", icon='LIGHT_SPOT').type='SPOT'
    row.operator("object.light_add", text="", icon='LIGHT_AREA').type='AREA'
    
    # Materials (Our Custom Operator)
    layout.label(text="Quick Materials")
    row = layout.row(align=True)
    
    # We can use colored icons or just text? 
    # Use standard icon 'MATERIAL' but distinctive colors if we could color the button... 
    # (Not possible in standard UI without custom icons).
    # We'll use the prompt logic: preset enums.
    
    op = row.operator("bfa.quick_material", text="", icon='MATERIAL')
    op.mat_type = 'PLASTIC'
    op.color_preset = 'WHITE'
    
    op = row.operator("bfa.quick_material", text="", icon='SHADING_TEXTURE') # Red
    op.mat_type = 'PLASTIC'
    op.color_preset = 'RED'

    op = row.operator("bfa.quick_material", text="", icon='SHADING_SOLID') # Blue
    op.mat_type = 'PLASTIC'
    op.color_preset = 'BLUE'

    op = row.operator("bfa.quick_material", text="", icon='SHADING_RENDERED') # Metal
    op.mat_type = 'METAL'
    op.color_preset = 'GREY'
    
    op = row.operator("bfa.quick_material", text="", icon='XRAY') # Glass
    op.mat_type = 'GLASS'
    op.color_preset = 'WHITE'


# Header Integration
def draw_header_shelf(self, context):
    layout = self.layout
    # Check preferences
    prefs = bpy.context.preferences.addons[__package__.split('.')[0]].preferences
    if not prefs.enable_shelf_header:
        return
        
    layout.separator()
    # Primitives Popover
    layout.popover(panel="VIEW3D_PT_bfa_shelf_popover", text="", icon='ADD')

class VIEW3D_PT_bfa_shelf_popover(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = "BFA Quick Create"

    def draw(self, context):
        layout = self.layout
        draw_shelf(layout)

classes = (
    BFA_PT_shelf,
    VIEW3D_PT_bfa_shelf_popover,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # Append to header
    bpy.types.VIEW3D_HT_header.append(draw_header_shelf)

def unregister():
    bpy.types.VIEW3D_HT_header.remove(draw_header_shelf)
    for cls in classes:
        bpy.utils.unregister_class(cls)
