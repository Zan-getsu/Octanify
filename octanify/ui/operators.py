"""Octanify — Operators.

Provides:
- OCTANIFY_OT_convert        — main conversion (active object or all)
- OCTANIFY_OT_update_selected_gamma — update gamma on active material
- OCTANIFY_OT_update_all_gamma     — update gamma on all converted materials
"""

from __future__ import annotations

import bpy

from ..core.conversion_engine import (
    convert_object_materials,
    convert_scene_materials,
    reset_cache,
)
from ..core.gamma_system import update_material_gamma, update_all_materials_gamma
from ..utils.logger import get_logger

log = get_logger()


# ---------------------------------------------------------------------------
# Convert operator
# ---------------------------------------------------------------------------

class OCTANIFY_OT_convert(bpy.types.Operator):
    """Convert Cycles materials to Octane materials"""

    bl_idname = "octanify.convert"
    bl_label = "Convert to Octane"
    bl_description = "Convert Cycles materials to Octane materials"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        if context.scene.octanify_batch_mode == "ACTIVE":
            return context.active_object is not None
        return True

    def execute(self, context: bpy.types.Context) -> set[str]:
        scene = context.scene
        batch_mode = scene.octanify_batch_mode
        gamma = scene.octanify_albedo_gamma

        try:
            if batch_mode == "ACTIVE":
                obj = context.active_object
                if obj is None:
                    self.report({"WARNING"}, "No active object selected")
                    return {"CANCELLED"}

                reset_cache()
                converted = convert_object_materials(obj, gamma_value=gamma)
                count = len(converted)
                self.report(
                    {"INFO"},
                    f"Converted {count} material(s) on '{obj.name}'",
                )

            else:  # ALL
                converted = convert_scene_materials(gamma_value=gamma)
                count = len(converted)
                self.report(
                    {"INFO"},
                    f"Converted {count} material(s) across all objects",
                )

        except Exception as exc:
            log.error("Conversion failed: %s", exc, exc_info=True)
            self.report({"ERROR"}, f"Conversion error: {exc}")
            return {"CANCELLED"}

        return {"FINISHED"}


# ---------------------------------------------------------------------------
# Update selected material gamma
# ---------------------------------------------------------------------------

class OCTANIFY_OT_update_selected_gamma(bpy.types.Operator):
    """Re-apply gamma correction to the active material"""

    bl_idname = "octanify.update_selected_gamma"
    bl_label = "Update Selected Material"
    bl_description = "Re-apply gamma correction to the active material"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        if obj is None:
            return False
        if not hasattr(obj, "active_material"):
            return False
        return obj.active_material is not None

    def execute(self, context: bpy.types.Context) -> set[str]:
        gamma = context.scene.octanify_albedo_gamma
        mat = context.active_object.active_material

        try:
            count = update_material_gamma(mat, gamma)
            self.report(
                {"INFO"},
                f"Updated gamma on {count} texture(s) in '{mat.name}'",
            )
        except Exception as exc:
            log.error("Gamma update failed: %s", exc, exc_info=True)
            self.report({"ERROR"}, f"Gamma update error: {exc}")
            return {"CANCELLED"}

        return {"FINISHED"}


# ---------------------------------------------------------------------------
# Update all materials gamma
# ---------------------------------------------------------------------------

class OCTANIFY_OT_update_all_gamma(bpy.types.Operator):
    """Re-apply gamma correction to all materials on the active object"""

    bl_idname = "octanify.update_all_gamma"
    bl_label = "Update All Materials"
    bl_description = "Re-apply gamma correction to all materials on the active object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and hasattr(obj, "material_slots")

    def execute(self, context: bpy.types.Context) -> set[str]:
        gamma = context.scene.octanify_albedo_gamma
        obj = context.active_object
        materials = [
            slot.material for slot in obj.material_slots
            if slot.material is not None
        ]

        try:
            count = update_all_materials_gamma(materials, gamma)
            self.report(
                {"INFO"},
                f"Updated gamma on {count} texture(s) across {len(materials)} material(s)",
            )
        except Exception as exc:
            log.error("Gamma update failed: %s", exc, exc_info=True)
            self.report({"ERROR"}, f"Gamma update error: {exc}")
            return {"CANCELLED"}

        return {"FINISHED"}


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

classes = (
    OCTANIFY_OT_convert,
    OCTANIFY_OT_update_selected_gamma,
    OCTANIFY_OT_update_all_gamma,
)


def register() -> None:
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
