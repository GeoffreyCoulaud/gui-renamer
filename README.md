# Pattern Renamer

A simple GUI file renamer using regexes built with python, GTK and LibAdwaita.

## Development Setup

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

2. Install dependencies depending on your platform

   <details>
   <summary>Arch Linux & EndeavourOS</summary>
   
   ```bash
   sudo pacman -Syu gtk4 libadwaita meson
   ```
   
   </details>

   <details>
   <summary>MacOS</summary>
   
   ```sh
   brew install gtk4 libadwaita cairo glib pygobject3 gobject-introspection meson
   ```
   
   </details>

3. Setup the project
   ```sh
   uv sync
   ```

4. Setup, compile and install
   ```sh
   meson setup build
   meson compile -C build
   meson install -C build
   ```

5. Run the app
   ```sh
   pattern-renamer
   ```