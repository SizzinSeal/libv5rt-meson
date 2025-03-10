project('v5rt', 'c',
    version: '1.0',
    default_options: ['warning_level=3'])

version = 'V5_20240802_15_00_00'
hash = '51fc8695402dd39d5713d20bda5d23699e85913d595e47cd550112ec290730a2'

keep_files = [
  'libv5rt.a',
  'v5_api.h',
  'v5_apitypes.h',
  'v5_apiuser.h',
  'v5_color.h'
]

keep_objects = [
  'v5_util.c.obj',
  'v5_apijump.c.obj',
  'v5_apiuser.c.obj',
  'v5_apigraphics.c.obj',
  'v5_apiversions.c.obj'
]

python = find_program('python3')

custom_target(
  'v5rt',
  input: 'get-libv5rt.py',
  output: keep_files,
  install: true,
  install_dir: 'subdir',
  command: [python, '@INPUT@', version, hash, keep_files, keep_objects]
)