# renamer

A simple GUI file renamer using regexes built with python, GTK and LibAdwaita.


## Development Setup

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

2. Install the GTK4 and LibAdwaita development libraries depending on your platform

    - Arch Linux & EndeavourOS
        ```bash
        sudo pacman -Syu gtk4 libadwaita
        ```

   - MacOS
      ```sh
      brew install gtk4 libadwaita cairo glib pygobject3 gobject-introspection
      ```

3. Setup the project:
   ```bash
   uv sync
   ```

4. Install the project in development mode:
   ```bash
   uv pip install -e .
   ```

5. You may now run the application:
   
   <details>
   <summary>MacOS specific tweaks</summary>

      You will need to run `export DYLD_LIBRARY_PATH=/opt/homebrew/lib` for the system 
      dependencies to be located properly with a `homebrew` install.  

      For this to persist, you may add `/opt/homebrew/lib` to your `DYLD_FALLBACK_LIBRARY_PATH`.

   </details>
   
   ```bash
   uv run gui-renamer
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