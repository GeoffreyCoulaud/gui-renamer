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

4. Setup, compile and install meson
   ```sh
   meson setup build
   meson compile -C build
   meson install -C build
   ```

5. Run the app
   ```sh
   pattern-renamer
   ```

## Updating the flatpak python requirements

1. Install the `flatpak-pip-generator` from the [flatpak buider tools repo](https://github.com/flatpak/flatpak-builder-tools)

```sh
wget https://raw.githubusercontent.com/flatpak/flatpak-builder-tools/refs/heads/master/pip/flatpak-pip-generator.py
chmod u+x flatpak-pip-generator.py
mv flatpak-pip-generator.py ~/.local/bin/flatpak-pip-generator
```

2. Add `~/.local/bin` to your `$PATH` if it's not already included
3. Update the dependencies file

```sh
flatpak-pip-generator \
  --runtime=$(jq -r '"\(.sdk)//\(.["runtime-version"])"' com.github.geoffreycoulaud.PatternRenamer.json) \
  --pyproject-file pyproject.toml \
  --output python3-requirements
```