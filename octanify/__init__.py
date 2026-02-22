"""Octanify — Cycles to Octane Material Converter

A production-grade Blender addon that converts Cycles shader trees
to Octane equivalents with full support for:

• Complex node chain traversal and reconstruction
• Glass, emission, bump, alpha, and volumetric handling
• Albedo gamma control with per-material update
• Object-level and scene-level batch conversion
• Procedural scale correction
• Duplicate material de-duplication
"""

from __future__ import annotations

# Legacy bl_info for compatibility with Blender's classic addon system.
# The blender_manifest.toml handles the newer extension system (4.2+).
bl_info = {
    "name": "Octanify",
    "author": "Niloy Bhowmick",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Octanify",
    "description": "Convert Cycles materials to Octane materials with one click",
    "category": "Material",
}

import bpy

from .ui import panel, operators


# ---------------------------------------------------------------------------
# Scene properties
# ---------------------------------------------------------------------------

def _register_properties() -> None:
    bpy.types.Scene.octanify_batch_mode = bpy.props.EnumProperty(
        name="Batch Mode",
        description="Which objects to convert",
        items=[
            ("ACTIVE", "Active Object", "Convert only the active object's materials"),
            ("ALL", "All Objects", "Convert all materials across all scene objects"),
        ],
        default="ACTIVE",
    )

    bpy.types.Scene.octanify_albedo_gamma = bpy.props.FloatProperty(
        name="Albedo Gamma",
        description="Gamma correction value for base color / albedo textures",
        default=2.2,
        min=0.1,
        max=3.0,
        step=10,
        precision=2,
    )


def _unregister_properties() -> None:
    del bpy.types.Scene.octanify_batch_mode
    del bpy.types.Scene.octanify_albedo_gamma


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def register() -> None:
    _register_properties()
    panel.register()
    operators.register()


def unregister() -> None:
    operators.unregister()
    panel.unregister()
    _unregister_properties()
