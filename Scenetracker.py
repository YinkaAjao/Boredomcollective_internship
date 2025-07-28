bl_info = {
    "name": "SceneTracker",
    "blender": (4, 3, 2),
    "location": "View3D > Sidebar > SceneTracker",
    "description": "Display object, vertex, face, and poly counts",
    "category": "3D View",
}

import bpy
from bpy.types import Panel

class ST_PT_Panel(Panel):
    bl_label = "Scene Tracker"
    bl_idname = "ST_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SceneTracker"

    def draw(self, context):
        layout = self.layout
        total_objects = len(bpy.context.scene.objects)
        total_verts = total_faces = 0

        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj_data = obj.data
                total_verts += len(obj_data.vertices)
                total_faces += len(obj_data.polygons)

        layout.label(text=f"Objects: {total_objects}")
        layout.label(text=f"Vertices: {total_verts}")
        layout.label(text=f"Polygons: {total_faces}")

def register():
    bpy.utils.register_class(ST_PT_Panel)

def unregister():
    bpy.utils.unregister_class(ST_PT_Panel)
        for obj in context.selected_objects:
            bounds = calculate_object_bounds(obj)
            if bounds:
                min_x, max_x, min_y, max_y = bounds
                cam = context.scene.camera
                if cam:
                    cam.location.x = (min_x + max_x) / 2
                    cam.location.y = (min_y + max_y) / 2
                    cam.location.z += 5  
                    cam.keyframe_insert(data_path="location")
        return {'FINISHED'}
    except Exception as e:
        self.report({'ERROR'}, str(e))
        return {'CANCELLED'}

if __name__ == "__main__":
    register()
