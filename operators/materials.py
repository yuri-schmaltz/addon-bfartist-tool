import bpy
import random

class BFA_OT_quick_material(bpy.types.Operator):
    """Create and assign a quick material"""
    bl_idname = "bfa.quick_material"
    bl_label = "Quick Material"
    bl_options = {'REGISTER', 'UNDO'}

    mat_type: bpy.props.EnumProperty(
        items=[
            ('PLASTIC', "Plastic", "Shiny colored plastic"),
            ('METAL', "Metal", "Metallic surface"),
            ('GLASS', "Glass", "Transparent glass"),
            ('EMISSION', "Emission", "Glowing surface"),
            ('CLAY', "Clay", "Matte clay surface"),
        ],
        default='PLASTIC'
    )
    
    color_preset: bpy.props.EnumProperty(
        items=[
            ('WHITE', "White", ""),
            ('GREY', "Grey", ""),
            ('BLACK', "Black", ""),
            ('RED', "Red", ""),
            ('GREEN', "Green", ""),
            ('BLUE', "Blue", ""),
            ('YELLOW', "Yellow", ""),
            ('CYAN', "Cyan", ""),
            ('MAGENTA', "Magenta", ""),
            ('RANDOM', "Random", ""),
        ],
        default='WHITE'
    )

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object active")
            return {'CANCELLED'}

        # Create Material
        mat_name = f"BFA_{self.mat_type}_{self.color_preset}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Clear default nodes
        nodes.clear()
        
        # Output
        node_out = nodes.new(type='ShaderNodeOutputMaterial')
        node_out.location = (400, 0)
        
        # Shader
        node_shader = nodes.new(type='ShaderNodeBsdfPrincipled')
        node_shader.location = (0, 0)
        
        links.new(node_shader.outputs[0], node_out.inputs[0])
        
        # Determine Color
        color = (1.0, 1.0, 1.0, 1.0)
        if self.color_preset == 'WHITE': color = (1.0, 1.0, 1.0, 1.0)
        elif self.color_preset == 'GREY': color = (0.5, 0.5, 0.5, 1.0)
        elif self.color_preset == 'BLACK': color = (0.05, 0.05, 0.05, 1.0)
        elif self.color_preset == 'RED': color = (0.8, 0.05, 0.05, 1.0)
        elif self.color_preset == 'GREEN': color = (0.05, 0.8, 0.05, 1.0)
        elif self.color_preset == 'BLUE': color = (0.05, 0.05, 0.8, 1.0)
        elif self.color_preset == 'YELLOW': color = (0.8, 0.8, 0.05, 1.0)
        elif self.color_preset == 'CYAN': color = (0.05, 0.8, 0.8, 1.0)
        elif self.color_preset == 'MAGENTA': color = (0.8, 0.05, 0.8, 1.0)
        elif self.color_preset == 'RANDOM': color = (random.random(), random.random(), random.random(), 1.0)
        
        # Set Properties
        if self.mat_type == 'PLASTIC':
            node_shader.inputs['Base Color'].default_value = color
            node_shader.inputs['Roughness'].default_value = 0.2
            node_shader.inputs['Specular IOR Level'].default_value = 0.5 # API changed in 4.0, keep generic for now
            # In 4.0 "Specular" input is "Specular IOR Level" or generic "Specular"? 
            # 3.6 uses 'Specular'. 4.0 uses 'Specular IOR Level'. 
            # Smart check:
            if 'Specular' in node_shader.inputs:
                node_shader.inputs['Specular'].default_value = 0.5
            
        elif self.mat_type == 'METAL':
            node_shader.inputs['Base Color'].default_value = color
            node_shader.inputs['Metallic'].default_value = 1.0
            node_shader.inputs['Roughness'].default_value = 0.1
            
        elif self.mat_type == 'GLASS':
            node_shader.inputs['Base Color'].default_value = color
            node_shader.inputs['Transmission'].default_value = 1.0 # 3.6
             # 4.0: Transmission Weight
            if 'Transmission Weight' in node_shader.inputs:
                 node_shader.inputs['Transmission Weight'].default_value = 1.0
            elif 'Transmission' in node_shader.inputs:
                 node_shader.inputs['Transmission'].default_value = 1.0
                 
            node_shader.inputs['Roughness'].default_value = 0.0
            
        elif self.mat_type == 'EMISSION':
            # Principled has emission, or use Emission node
            node_shader.inputs['Emission Color'].default_value = color # 4.0 compatible?
            # 3.6: Emission. 4.0: Emission Color
            if 'Emission' in node_shader.inputs: # Old principled
                 node_shader.inputs['Emission'].default_value = color
            elif 'Emission Color' in node_shader.inputs:
                 node_shader.inputs['Emission Color'].default_value = color
                 
            node_shader.inputs['Emission Strength'].default_value = 5.0
            
        elif self.mat_type == 'CLAY':
            node_shader.inputs['Base Color'].default_value = color
            node_shader.inputs['Roughness'].default_value = 0.9
            node_shader.inputs['Metallic'].default_value = 0.0
            if 'Specular' in node_shader.inputs:
                node_shader.inputs['Specular'].default_value = 0.1

        # Assign to Object
        if obj.data.materials:
            # Replace active
            obj.data.materials[obj.active_material_index] = mat
        else:
            obj.data.materials.append(mat)

        return {'FINISHED'}

classes = (
    BFA_OT_quick_material,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
