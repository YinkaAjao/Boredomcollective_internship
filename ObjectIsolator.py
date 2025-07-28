bl_info = {
    "name": "ObjectIsolator",
    "blender": (4, 3, 2),
    "category": "Object",
    "author": "Your Name",
    "description": "Isolate selected objects by hiding others"
}

import bpy

class OBJECTISOLATOR_PT_panel(bpy.types.Panel):
    bl_label = "Object Isolator"
    bl_idname = "OBJECTISOLATOR_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ObjectIsolator'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.isolate_selected")
        layout.operator("object.unhide_all")

class OBJECTISOLATOR_OT_isolate(bpy.types.Operator):
    bl_idname = "object.isolate_selected"
    bl_label = "Isolate Selected"

    def execute(self, context):
        selected = context.selected_objects
        for obj in context.scene.objects:
            obj.hide_set(obj not in selected)
        return {'FINISHED'}

class OBJECTISOLATOR_OT_unhide(bpy.types.Operator):
    bl_idname = "object.unhide_all"
    bl_label = "Unhide All Objects"

    def execute(self, context):
        for obj in context.scene.objects:
            obj.hide_set(False)
        return {'FINISHED'}

classes = [OBJECTISOLATOR_PT_panel, OBJECTISOLATOR_OT_isolate, OBJECTISOLATOR_OT_unhide]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
