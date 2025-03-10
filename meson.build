project('v5rt', 'c',
    version: '1.0',
    default_options: ['warning_level=3'])

version = 'V5_20240802_15_00_00'
hash = '51FC8695402DD39D5713D20BDA5D23699E85913D595E47CD550112EC290730A2'

keep_files = [
  'libv5rt.a',
  'v5_api.h',
  'v5_apitypes.h',
  'v5_apiuser.h',
  'v5_color.h'
]

keep_objects = [
  'v5_fstubs.c.obj',
  'v5_util.c.obj',
  'v5_apijump.c.obj',
  'v5_apiuser.c.obj',
  'v5_apigraphics.c.obj',
  'v5_apiversions.c.obj'
]

python = find_program('python3')

custom_target(
  'get-libv5rt.py',
  input: 'get-libv5rt.py',
  output: keep_files,
  install: true,
  install_dir: 'subdir',
  command: [python, '@INPUT@', version, hash, keep_files, keep_objects]
)