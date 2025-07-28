bl_info = {
    "name": "LightManager",
    "version": (2),
    "blender": (4, 3, 2),
    "location": "View3D > Sidebar > LightManager",
    "description": "Easily solo, rename, and adjust lights",
    "category": "Lighting",
}

import bpy
from bpy.types import Operator, Panel

class LM_OT_SoloLight(Operator):
    bl_idname = "lightmanager.solo_light"
    bl_label = "Solo Selected Light"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        if not selected or selected[0].type != 'LIGHT':
            self.report({'WARNING'}, "Select one light")
            return {'CANCELLED'}
        for obj in context.scene.objects:
            if obj.type == 'LIGHT':
                obj.hide_render = obj != selected[0]
                obj.hide_viewport = obj != selected[0]
        self.report({'INFO'}, f"Soloed: {selected[0].name}")
        return {'FINISHED'}

class LM_PT_Panel(Panel):
    bl_label = "Light Manager"
    bl_idname = "LM_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "LightManager"

    def draw(self, context):
        layout = self.layout
        layout.operator(LM_OT_SoloLight.bl_idname)

def register():
    bpy.utils.register_class(LM_OT_SoloLight)
    bpy.utils.register_class(LM_PT_Panel)

def unregister():
    bpy.utils.unregister_class(LM_OT_SoloLight)
    bpy.utils.unregister_class(LM_PT_Panel)

if __name__ == "__main__":
    register()
