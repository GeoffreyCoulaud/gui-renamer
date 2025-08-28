gnome.compile_resources(
  'gresource.xml.in',
  '@0@.gresource.xml'.format(app_slug),
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

desktop_file = i18n.merge_file(
  input: 'desktop.in',
  output: '@0@.desktop'.format(app_id),
  type: 'desktop',
  po_dir: './po',
  install: true,
  install_dir: get_option('datadir') / 'applications',
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

appstream_file = i18n.merge_file(
  input: 'metainfo.xml.in',
  output: '@0@.metainfo.xml'.format(app_id),
  po_dir: './po',
  install: true,
  install_dir: get_option('datadir') / 'metainfo',
)
appstreamcli = find_program('appstreamcli', required: false, disabler: true)
test(
  'Validate appstream file',
  appstreamcli,
  args: ['validate', '--no-net', '--explain', appstream_file],
)

configure_file(
  input: 'gschema.xml.in',
  output: '@0@.gschema.xml'.format(app_id),
  configuration: conf,
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas',
)
compile_schemas = find_program('glib-compile-schemas', required: false, disabler: true)
test(
  'Validate schema file',
  compile_schemas,
  args: ['--strict', '--dry-run', meson.current_source_dir()],
)

service_conf = configuration_data()
service_conf.set('bindir', get_option('prefix') / get_option('bindir'))
configure_file(
  input: 'service.in',
  output: '@0@.service'.format(app_id),
  configuration: service_conf,
  install_dir: get_option('datadir') / 'dbus-1' / 'services',
)

subdir('po')
subdir('icons')