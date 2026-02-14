import bpy

def menu_func_view3d_view(self, context):
    self.layout.separator()
    self.layout.operator("bfa.reset_3d_view", text="Reset 3D View", icon='VIEW3D')

def menu_func_view3d_shading(self, context):
    self.layout.separator()
    self.layout.operator("bfa.toggle_silhouette", text="Toggle Silhouette", icon='SHADING_SOLID')

def menu_func_mesh_transform(self, context):
    self.layout.separator()
    self.layout.operator("bfa.set_dimensions", text="Set Dimensions", icon='FIXED_SIZE')

def menu_func_mesh_delete(self, context):
    self.layout.separator()
    self.layout.operator("bfa.smart_delete", text="Smart Delete", icon='X')

def register():
    bpy.types.VIEW3D_MT_view.append(menu_func_view3d_view)
    # Viewport Shading menu is usually in the header, accessible via popover
    # There isn't a single "Shading" menu class that is universally used for the dropdown,
    # it's often VIEW3D_PT_shading... but let's try appending to the View menu or specific shading popovers.
    # The prompt asked for "Viewport Shading/Overlays".
    # VIEW3D_POPOVER_shading_rendering might be it? Or VIEW3D_PT_shading.
    # Actually, appending to `VIEW3D_MT_view` is safe.
    # For Shading/Overlays, it's a bit harder to inject into the popovers via python API cleanly without re-defining them.
    # Let's put Silhouette in View menu as well for now, or View > Viewport Shading if it exists.
    # Actually, let's put it in the "View" menu for simplicity and reliability.
    
    # For Overlays, it's VIEW3D_PT_overlay.
    
    bpy.types.VIEW3D_MT_transform.append(menu_func_mesh_transform)
    bpy.types.VIEW3D_MT_edit_mesh_delete.append(menu_func_mesh_delete)

    # Optional: Header button for Reset View?
    # Handled by preferences usually. We register the draw function, but we check preferences inside it?
    # Or we register/unregister based on preferences update.
    pass

def unregister():
    bpy.types.VIEW3D_MT_view.remove(menu_func_view3d_view)
    bpy.types.VIEW3D_MT_transform.remove(menu_func_mesh_transform)
    bpy.types.VIEW3D_MT_edit_mesh_delete.remove(menu_func_mesh_delete)
