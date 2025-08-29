This directory contains the packaging-specific files for Flatpak distribution. 

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
  --runtime=$(jq -r '"\(.sdk)//\(.["runtime-version"])"' com.github.geoffreycoulaud.PatternRenamer.Devel.json) \
  --pyproject-file ../../pyproject.toml \
  --output python3-requirements
```