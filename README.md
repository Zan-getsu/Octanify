<p align="center">
  <h1 align="center">⚡ Octanify</h1>
  <p align="center">
    <strong>One-click Cycles → Octane material conversion for Blender</strong>
  </p>
  <p align="center">
    <a href="#features">Features</a> •
    <a href="#installation">Installation</a> •
    <a href="#usage">Usage</a> •
    <a href="#how-it-works">How It Works</a> •
    <a href="#supported-nodes">Supported Nodes</a>
  </p>
</p>

---

**Octanify** is a production-grade Blender addon that intelligently converts Cycles material trees into Octane equivalents — preserving shader intent, texture chains, and procedural structure with a single click.

> No manual node rewiring. No broken links. Just convert and render.

## Features

| Feature | Description |
|---|---|
| 🎯 **Principled BSDF** | Full 20+ input mapping to Universal Material |
| 🔗 **Link Reconstruction** | Rebuilds all node connections with 7-strategy socket matching |
| 🪟 **Glass & Transmission** | Auto-detects transmission > 0.5 and configures specular mode |
| 💡 **Emission** | Auto-inserts Octane TextureEmission node for proper emission rendering |
| 🌫️ **Volumetrics** | Volume Absorption/Scatter → Octane Medium nodes |
| 🗺️ **Normal & Bump** | Direct-connects normal map textures to material Normal input |
| 🎨 **Albedo Gamma** | Per-material gamma control with live update slider |
| 📦 **Batch Conversion** | Convert active object or entire scene in one click |
| 🔄 **Smart Deduplication** | Caches converted materials — no duplicate work |
| 📐 **Scale Correction** | Adjusts procedural textures for object scale |
| 🧩 **Transparent Passthrough** | SeparateColor, Math, RGB Curves pass through cleanly |

## Installation

### Blender 4.2+ / 5.0 (Extension System)
1. Download `octanify.zip`
2. Open Blender → `Edit → Preferences → Extensions`
3. Click the dropdown arrow → **Install from Disk**
4. Select `octanify.zip`
5. Enable **Octanify**

### Requirements
- **Blender** 4.2 or later
- **OctaneRender** plugin for Blender (required for Octane node creation)

## Usage

1. Press `N` in the **3D Viewport** or **Shader Editor** to open the sidebar
2. Switch to the **Octanify** tab
3. Select **Active Object** or **All Objects** batch mode
4. Adjust the **Albedo Gamma** slider (default: 2.2)
5. Click **Convert to Octane** ⚡

Your original Cycles materials are preserved — Octanify creates `<material_name>_OCTANE` duplicates and assigns them automatically.

### Updating Gamma
After conversion, you can re-adjust gamma at any time:
- **Update Selected Material** — applies to the active material
- **Update All Materials** — applies to all materials on the selected object

## How It Works

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Analyze    │────▶│    Create    │────▶│   Transfer   │
│  Cycles Tree │     │ Octane Nodes │     │  Properties  │
└──────────────┘     └──────────────┘     └──────────────┘
                                                │
┌──────────────┐     ┌──────────────┐           ▼
│   Apply      │◀────│    Post-     │◀────┌──────────────┐
│   Gamma      │     │   Process    │     │   Rebuild    │
└──────────────┘     └──────────────┘     │    Links     │
                                          └──────────────┘
```

1. **Analyze** — Snapshot the Cycles node tree (nodes, links, properties, patterns)
2. **Schedule** — Topological sort ensures dependencies are created first
3. **Create** — Instantiate Octane equivalents using runtime-resolved `bl_idname` candidates
4. **Transfer** — 30+ per-type handlers map Cycles values → Octane parameters
5. **Rebuild** — 7-strategy socket resolution reconnects all links
6. **Post-process** — Fix MixShader order, insert emission nodes, handle Normal/Bump fallbacks, alpha/opacity, volumetrics
7. **Gamma** — Apply albedo gamma correction (skips non-color textures)

## Supported Nodes

<details>
<summary><strong>Shaders (9 types)</strong></summary>

- Principled BSDF → Universal Material
- Glass BSDF → Specular Material
- Glossy BSDF → Glossy Material
- Diffuse BSDF → Diffuse Material
- Emission → Diffuse Material + TextureEmission
- Transparent BSDF → Null Material
- Translucent BSDF → Diffuse Material
- Refraction BSDF → Specular Material
- Mix Shader → Mix Material (with auto slot swap)
</details>

<details>
<summary><strong>Textures (8 types)</strong></summary>

- Image Texture → Octane Image Texture (with colorspace/gamma handling)
- Noise → Octane Noise
- Voronoi → Octane Voronoi
- Wave → Octane Wave
- Musgrave → Octane Noise
- Checker → Octane Checks
- Brick → Octane Marble
- Gradient → Octane Gradient
</details>

<details>
<summary><strong>Input / Vector (12 types)</strong></summary>

- Mapping → 3D Transform
- Texture Coordinate → Mesh UV Projection
- UV Map → Mesh UV Projection
- Normal Map → direct connection to Normal input
- Bump → Octane Bump Texture
- Displacement → Octane Displacement
- RGB → Octane RGB Color
- Value → Octane Float Value
- Fresnel / Layer Weight → Octane Fresnel
- Vertex Color → Octane Color Vertex Attribute
- Attribute → Octane Attribute
- Ambient Occlusion → Octane Dirt Texture
</details>

<details>
<summary><strong>Transparent Passthrough (handled inline)</strong></summary>

- Separate Color / RGB / XYZ — flattened, source texture passes through
- Combine Color / RGB / XYZ — flattened
- RGB Curves, Hue/Saturation, Brightness/Contrast, Gamma — passthrough
- Math, Map Range, Clamp, Invert — passthrough
</details>

## Project Structure

```
octanify/
├── __init__.py                 # Entry point, bl_info, scene properties
├── blender_manifest.toml       # Blender 4.2+ extension manifest
├── core/
│   ├── node_registry.py        # 40+ Cycles → Octane node mappings
│   ├── shader_detection.py     # Tree analysis, reroute & transparent flattening
│   ├── graph_engine.py         # Dependency scheduling & node creation
│   ├── property_mapper.py      # 30+ per-type value transfer handlers
│   ├── conversion_engine.py    # Main orchestrator pipeline
│   ├── gamma_system.py         # Albedo gamma correction
│   └── volumetric_handler.py   # Volume → Octane medium handling
├── ui/
│   ├── panel.py                # N-Panel (3D Viewport + Shader Editor)
│   └── operators.py            # Convert & gamma update operators
└── utils/
    ├── logger.py               # Console logging
    └── cache.py                # Material dedup cache
```

## 🙏 Credits

- Architecture inspired by analysis of [cycles2octane](https://github.com/RodrigoGama1902/cycles2octane) by Rodrigo Gama

## License

GPL-3.0-or-later — Compatible with Blender's licensing requirements.

---

<p align="center">
  <sub>Built with ☕ by <strong>Niloy Bhowmick</strong></sub>
</p>
