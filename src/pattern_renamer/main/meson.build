configure_file(
  input: 'pattern-renamer.in',
  output: app_executable_name,
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x',
)

install_data(
  [
    configure_file(
      input: 'build_constants.py.in',
      output: 'build_constants.py',
      configuration: conf,
    ),
    '__init__.py',
    'app.py',
    'main_model.py',
  ],
  install_dir: moduledir / 'main',
)
install_subdir('types', install_dir: moduledir / 'main')
install_subdir('ui', install_dir: moduledir / 'main')