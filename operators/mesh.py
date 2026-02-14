import bpy
import bmesh
from mathutils import Vector

class BFA_OT_set_dimensions(bpy.types.Operator):
    """Set absolute dimensions for selection in World Space"""
    bl_idname = "bfa.set_dimensions"
    bl_label = "Set Dimensions"
    bl_options = {'REGISTER', 'UNDO'}

    # Dimensions
    target_x: bpy.props.FloatProperty(name="X", unit='LENGTH', min=0.0)
    target_y: bpy.props.FloatProperty(name="Y", unit='LENGTH', min=0.0)
    target_z: bpy.props.FloatProperty(name="Z", unit='LENGTH', min=0.0)

    # Toggles to enable/disable specific axis modification
    use_x: bpy.props.BoolProperty(name="Axis X", default=True)
    use_y: bpy.props.BoolProperty(name="Axis Y", default=True)
    use_z: bpy.props.BoolProperty(name="Axis Z", default=True)

    pivot_point: bpy.props.EnumProperty(
        name="Pivot",
        items=[
            ('MEDIAN', "Median Point", "Center of selection geometry"),
            ('BOUNDS_CENTER', "Bounds Center", "Center of the bounding box"),
            ('CURSOR', "3D Cursor", "Use 3D Cursor as pivot"),
            ('ACTIVE', "Active Element", "Use Active Element location")
        ],
        default='BOUNDS_CENTER'
    )

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'MESH' and context.mode == 'EDIT_MESH')

    def invoke(self, context, event):
        # Initialize properties with current dimensions
        # This is a bit complex in Execute/Invoke pattern because calculating dims requires BMESH access.
        # But we want the UI to show current dims when operator starts.
        # For simplicity in 'Redo Panel', we just rely on defaults or last used?
        # A better UX for "Set Dimensions" is to read current dims FIRST.
        
        # We can do this by getting the selection bounds in Invoke.
        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        selected_verts = [v for v in bm.verts if v.select]
        if not selected_verts:
            self.report({'WARNING'}, "No vertices selected")
            return {'CANCELLED'}

        # Calculate bounds in WORLD space
        mat_world = obj.matrix_world
        
        # We need efficient min/max
        # Convert coords to world
        world_coords = [mat_world @ v.co for v in selected_verts]
        
        min_x = min(v.x for v in world_coords)
        max_x = max(v.x for v in world_coords)
        min_y = min(v.y for v in world_coords)
        max_y = max(v.y for v in world_coords)
        min_z = min(v.z for v in world_coords)
        max_z = max(v.z for v in world_coords)
        
        dims = Vector((max_x - min_x, max_y - min_y, max_z - min_z))
        
        self.target_x = dims.x
        self.target_y = dims.y
        self.target_z = dims.z
        
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        selected_verts = [v for v in bm.verts if v.select]
        if not selected_verts:
            return {'CANCELLED'}

        mat_world = obj.matrix_world
        world_coords = [mat_world @ v.co for v in selected_verts]
        
        min_x = min(v.x for v in world_coords)
        max_x = max(v.x for v in world_coords)
        min_y = min(v.y for v in world_coords)
        max_y = max(v.y for v in world_coords)
        min_z = min(v.z for v in world_coords)
        max_z = max(v.z for v in world_coords)
        
        current_dims = Vector((max_x - min_x, max_y - min_y, max_z - min_z))
        center = Vector(((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2))
        
        # Determine Transformation Pivot
        pivot = center # Default BOUNDS_CENTER
        
        if self.pivot_point == 'MEDIAN':
            # Median of vertices locations
            # Average of logical coordinates
            pivot = sum((v for v in world_coords), Vector()) / len(world_coords)
            
        elif self.pivot_point == 'CURSOR':
            pivot = context.scene.cursor.location
            
        elif self.pivot_point == 'ACTIVE':
            elem = bm.select_history.active
            if elem and isinstance(elem, bmesh.types.BMVert):
                pivot = mat_world @ elem.co
            # Handle edge/face active?
            # For simplicity, if not vert, fallback to Bounds? Or finding center of active face/edge.
        
        # Calculate Scale Factors
        scale_x = 1.0
        scale_y = 1.0
        scale_z = 1.0
        
        # Helper to avoid division by zero
        def get_scale(current, target):
            if current < 1e-6: return 1.0 # Cannot scale zero dimension
            return target / current
            
        if self.use_x: scale_x = get_scale(current_dims.x, self.target_x)
        if self.use_y: scale_y = get_scale(current_dims.y, self.target_y)
        if self.use_z: scale_z = get_scale(current_dims.z, self.target_z)
        
        # Apply Scaling
        # To scale in place relative to Pivot:
        # P' = Pivot + S * (P - Pivot)
        
        # We need to apply this to all selected vertices
        # And convert back to Local Space (since we modify v.co)
        
        # Scale Matrix
        # M_scale = Matrix.Scale(sx, 4, (1,0,0)) @ ... but easier to just do vector math
        
        mat_world_inv = mat_world.inverted()
        
        # If Pivot is in world space, we can do calculation in world space then transform back?
        # Or transform pivot to local space?
        # Doing logic in Local Space:
        # We computed scale based on World Dimensions, which is correct (users think in World Units).
        # We computed Pivot in World Space.
        
        # Let's perform transform on local coordinates using local pivot and scale?
        # Wait, if object is rotated, World X scale != Local X scale.
        # "Set Dimensions" usually implies "Bounding Box aligned to World Axes" for World Dimensions
        # OR "Bounding Box aligned to Object Axes" for Local Dimensions.
        # The requirement says "Absolute Dimensions in World Coordinates".
        # This implies we measure along World Axes and scale along World Axes.
        
        for v in selected_verts:
            p_world = mat_world @ v.co
            
            # Apply scale relative to pivot
            diff = p_world - pivot
            diff.x *= scale_x
            diff.y *= scale_y
            diff.z *= scale_z
            
            new_p_world = pivot + diff
            
            # Write back to local
            v.co = mat_world_inv @ new_p_world
            
        bmesh.update_edit_mesh(me)
        return {'FINISHED'}


class BFA_OT_smart_delete(bpy.types.Operator):
    """Context Aware Delete based on selection mode"""
    bl_idname = "bfa.smart_delete"
    bl_label = "Smart Delete"
    bl_options = {'REGISTER', 'UNDO'}

    dissolve: bpy.props.BoolProperty(
        name="Dissolve",
        description="Dissolve geometry instead of deleting",
        default=False
    )

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'MESH' and context.mode == 'EDIT_MESH')

    def execute(self, context):
        # Determine selection mode
        # context.tool_settings.mesh_select_mode is a list [Vert, Edge, Face]
        select_mode = context.tool_settings.mesh_select_mode
        
        vert_mode = select_mode[0]
        edge_mode = select_mode[1]
        face_mode = select_mode[2]

        # Order of precedence if multiple are active (e.g. shift-click modes):
        # Face > Edge > Vert is usually "safer" or more comprehensive.
        
        target_mode = 'VERT'
        if face_mode:
            target_mode = 'FACE'
        elif edge_mode:
            target_mode = 'EDGE'
        elif vert_mode:
            target_mode = 'VERT'
            
        # Call standard delete/dissolve ops
        if self.dissolve:
             if target_mode == 'VERT':
                 bpy.ops.mesh.dissolve_verts()
             elif target_mode == 'EDGE':
                 bpy.ops.mesh.dissolve_edges()
             elif target_mode == 'FACE':
                 bpy.ops.mesh.dissolve_faces()
        else:
             if target_mode == 'VERT':
                 bpy.ops.mesh.delete(type='VERT')
             elif target_mode == 'EDGE':
                 bpy.ops.mesh.delete(type='EDGE')
             elif target_mode == 'FACE':
                 bpy.ops.mesh.delete(type='FACE')
        
        return {'FINISHED'}

classes = (
    BFA_OT_set_dimensions,
    BFA_OT_smart_delete,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
