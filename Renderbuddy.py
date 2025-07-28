bl_info = {
    "name": "RenderBuddy",
    "version": (4),
    "blender": (4, 3, 2),
    "location": "View3D > Sidebar > RenderBuddy",
    "description": "One-click tools for still image rendering",
    "category": "Render",
}

import bpy
from bpy.props import (EnumProperty, FloatProperty, 
                      StringProperty, PointerProperty)
from bpy.types import (Operator, Panel, PropertyGroup)

# ------------------------------------------------------------------------
# Core Functions
# ------------------------------------------------------------------------
def calculate_object_bounds(obj):
    """Returns (min_x, max_x, min_y, max_y) in camera space"""
    if not obj or obj.type not in {'MESH', 'EMPTY'}:
        return None
    
    # Get object bounds in world space
    matrix = obj.matrix_world
    bound_box = obj.bound_box if hasattr(obj, 'bound_box') else [
        (-1,-1,-1), (1,1,1)]  # Fallback for empties
    
    # Convert to camera space
    cam = bpy.context.scene.camera
    if not cam:
        return None
    
    cam_matrix = cam.matrix_world.inverted()
    points = [cam_matrix @ matrix @ Vector(corner) for corner in bound_box]
    
    # Get 2D bounds (ignoring Z-axis)
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)
    
    return (min_x, max_x, min_y, max_y)

# ------------------------------------------------------------------------
# Operators
# ------------------------------------------------------------------------
class RB_OT_ReframeCamera(Operator):
    bl_idname = "renderbuddy.reframe_camera"
    bl_label = "Reframe Shot"
    bl_options = {'REGISTER', 'UNDO'}
    
    padding: FloatProperty(
        name="Padding", 
        default=0.1, min=0.0, max=1.0,
        description="Empty space around subject"
    )
    
    def execute(self, context):
        try:
            cam = context.scene.camera
            if not cam:
                raise Exception("No active camera")
            
            selected = context.selected_objects
            if not selected:
                raise Exception("No objects selected")
            
            # Calculate combined bounds
            all_bounds = []
            for obj in selected:
                bounds = calculate_object_bounds(obj)
                if bounds:
                    all_bounds.append(bounds)
            
            if not all_bounds:
                raise Exception("No valid bounds calculated")
            
            # Find total bounds with padding
            min_x = min(b[0] for b in all_bounds) * (1 - self.padding)
            max_x = max(b[1] for b in all_bounds) * (1 + self.padding)
            min_y = min(b[2] for b in all_bounds) * (1 - self.padding)
            max_y = max(b[3] for b in all_bounds) * (1 + self.padding)
            
            # Adjust camera shift and lens
            cam.data.shift_x = (min_x + max_x) / 2
            cam.data.shift_y = (min_y + max_y) / 2
            cam.data.lens *= 0.9 * min(
                (max_x - min_x),
                (max_y - min_y)
            )
            
            self.report({'INFO'}, f"Reframed {len(selected)} objects")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

class RB_OT_MultiSizeRender(Operator):
    bl_idname = "renderbuddy.multi_size_render"
    bl_label = "Multi-Size Render"
    
    resolutions: StringProperty(
        name="Resolutions",
        default="1920x1080,1080x1080,800x600",
        description="Comma-separated WxH values"
    )
    
    def execute(self, context):
        original = {
            'res_x': context.scene.render.resolution_x,
            'res_y': context.scene.render.resolution_y,
            'filepath': context.scene.render.filepath
        }
        
        successes = 0
        for i, res in enumerate(self.resolutions.split(',')):
            try:
                w, h = map(int, res.strip().lower().split('x'))
                context.scene.render.resolution_x = w
                context.scene.render.resolution_y = h
                
                # Auto-number files
                context.scene.render.filepath = f"{original['filepath']}_{w}x{h}"
                bpy.ops.render.render(write_still=True)
                successes += 1
            except:
                self.report({'WARNING'}, f"Invalid resolution: {res}")
        
        # Restore original
        context.scene.render.resolution_x = original['res_x']
        context.scene.render.resolution_y = original['res_y']
        context.scene.render.filepath = original['filepath']
        
        self.report({'INFO'}, f"Rendered {successes} sizes")
        return {'FINISHED'}

# ------------------------------------------------------------------------
# UI
# ------------------------------------------------------------------------
class RB_PT_MainPanel(Panel):
    bl_label = "RenderBuddy"
    bl_idname = "RB_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "RenderBuddy"
    
    def draw(self, context):
        layout = self.layout
        
        # Framing Section
        box = layout.box()
        box.label(text="Camera Tools")
        box.operator(RB_OT_ReframeCamera.bl_idname, icon='VIEW_CAMERA')
        
        # Rendering Section
        box = layout.box()
        box.label(text="Batch Rendering")
        op = box.operator(RB_OT_MultiSizeRender.bl_idname, icon='RENDER_RESULT')
        op.resolutions = "1920x1080, 1080x1080, 800x600"

# ------------------------------------------------------------------------
# Registration
# ------------------------------------------------------------------------
classes = (
    RB_OT_ReframeCamera,
    RB_OT_MultiSizeRender,
    RB_PT_MainPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()