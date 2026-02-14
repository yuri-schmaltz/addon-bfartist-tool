# BFA Tools for Blender

A collection of usability tools ported from **Bforartists** to official **Blender 3.6+**. This addon aims to reduce friction and improve workflow efficiency with tools like Reset 3D View, Silhouette Toggle, Set Dimensions, and Smart Delete.

## Installation
1. Download the repository as a ZIP file (or release package).
2. In Blender, go to **Edit > Preferences > Add-ons**.
3. Click **Install...** and select the ZIP file.
4. Enable the addon **"BFA Tools for Blender"**.
5. You will find the **"BFA Tools"** tab in the 3D View Sidebar (N-Panel).

## Features

### 1. Viewport Tools
Located in the **Viewport** section of the BFA Tools panel.

- **Reset 3D View**: Instantly resets the viewport camera to a standard "Front" view (Location: 0,0,0, Rotation: Front, Zoom: Default).
  - *Option*: "Align to Front" (Default: On)
  - *Option*: "Use Perspective" (Default: Perspective)
  - Accessible via **View > Reset 3D View**.

- **Silhouette Toggle**: Toggles a "Silhouette" mode to check your mesh's outline and form.
  - Swaps shading to Flat/Single Color and disables shadows/cavity.
  - Accessible via **View > Toggle Silhouette**.

### 2. Modeling Tools (Edit Mode)
Located in the **Edit Mode** section of the BFA Tools panel.

- **Set Dimensions**: Set absolute World dimensions (X, Y, Z) for your selection.
  - Works on selected vertices/edges/faces.
  - Accounts for object rotation and scale.
  - Accessible via **Mesh > Transform > Set Dimensions**.

- **Smart Delete**: Context-aware delete tool.
  - **Vertices**: Dissolves or Deletes vertices.
  - **Edges**: Dissolves or Deletes edges.
  - **Faces**: Dissolves or Deletes faces.
  - Default shortcut: `Ctrl+Delete` (Optional in Preferences).
  - Accessible via **Mesh > Delete > Smart Delete**.

### 3. Quick Create Shelf
Located in the **Quick Create** section of the BFA Tools panel (and optionally in the Header).
- **Primitives**: Quick access to add common primitives (Cube, Sphere, Cylinder, etc.).
- **Lights**: Quick access to add lights (Point, Sun, Spot, Area).
- **Quick Materials**: One-click creation and assignment of basic materials (Plastic, Metal, Glass, etc.).

## Preferences
Go to **Edit > Preferences > Add-ons > BFA Tools for Blender** to configure:
- **Enable Menu Entries**: Add tools to standard Blender menus.
- **Enable Header Button**: Add "Reset View" button to the 3D View header.
- **Enable Quick Shelf in Header**: Add "Quick Create" popover to the 3D View header.
- **Enable Keymaps**: Enable custom shortcuts (e.g., Ctrl+Delete).

## Compatibility
- **Blender 3.6 LTS**: Fully Supported.
- **Blender 4.x**: Supported (API changes monitored).
- **Blender 5.x**: To be determined.

## License
GPL v3 (Compatible with Blender).