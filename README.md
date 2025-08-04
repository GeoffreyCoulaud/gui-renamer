# renamer

A simple GUI file renamer using regexes built with python, GTK and LibAdwaita.


## Development Setup

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

2. Install the GTK4 and LibAdwaita development libraries depending on your platform

    - Arch Linux & EndeavourOS
        ```bash
        sudo pacman -Syu gtk4 libadwaita
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
    ```bash
    uv run renamer
    ```