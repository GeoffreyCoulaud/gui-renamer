project(
  'pattern-renamer',
  version: '1.0.0',
  meson_version: '>= 1.1.0',
  default_options: [
    'werror=true',
  ],
)

dependency('gtk4', version: '>= 4.15.0')
dependency('libadwaita-1', version: '>= 1.7.5')

i18n = import('i18n')
gnome = import('gnome')
python = import('python')
py_installation = python.find_installation('python3')
python_dir = join_paths(get_option('prefix'), py_installation.get_install_dir())
moduledir = python_dir / 'pattern_renamer'
pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
libexecdir = join_paths(get_option('prefix'), get_option('libexecdir'))
profile = get_option('profile')
if profile == 'development'
  app_id = 'com.github.geoffreycoulaud.PatternRenamer.Devel'
  prefix = '/com/github/geoffreycoulaud/PatternRenamer/Devel/'
elif profile == 'release'
  app_id = 'com.github.geoffreycoulaud.PatternRenamer'
  prefix = '/com/github/geoffreycoulaud/PatternRenamer/'
endif
app_executable_name = 'pattern-renamer'
app_slug = 'pattern-renamer'
app_name = 'Pattern Renamer'

conf = configuration_data()
conf.set('VERSION', meson.project_version())
conf.set('PYTHON', py_installation.full_path())
conf.set('PYTHON_VERSION', py_installation.language_version())
conf.set('LOCALEDIR', get_option('prefix') / get_option('localedir'))
conf.set('BINDIR', get_option('prefix') / get_option('bindir'))
conf.set('APP_EXECUTABLE_NAME', app_executable_name)
conf.set('APP_SLUG', app_slug)
conf.set('APP_NAME', app_name)
conf.set('APP_ID', app_id)
conf.set('PREFIX', prefix)
conf.set('PROFILE', profile)
conf.set('PKGDATADIR', pkgdatadir)
conf.set('LIBEXECDIR', libexecdir)
conf.set('PYTHONDIR', python_dir)

subdir('data')
subdir('src')

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)