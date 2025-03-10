project('v5', 'c',
    version: '1.0',
    default_options: ['warning_level=3'])

version = 'V5_20240802_15_00_00'
hash = '51fc8695402dd39d5713d20bda5d23699e85913d595e47cd550112ec290730a2'

keep_object_files = [
  'v5_util.c.obj',
  'v5_apijump.c.obj',
  'v5_apiuser.c.obj',
  'v5_apigraphics.c.obj',
  'v5_apiversions.c.obj'
]

python = find_program('python3')

libv5rt = custom_target(
  'libv5rt',
  input: 'get-libv5rt.py',
  output: [
    'libv5rt.a',
    'v5_api.h',
    'v5_apitypes.h',
    'v5_apiuser.h',
    'v5_color.h'
  ],
  command: [python, '@INPUT@', version, hash, '@OUTPUT@', '@OUTDIR@']
)

patch_headers = custom_target(
  'patch-headers',
  input: ['patch-headers.py', libv5rt],
  output: [
    'v5_api_patched.h',
    'v5_apitypes_patched.h',
    'v5_apiuser_patched.h',
    'v5_color_patched.h',
  ],
  command: [python, '@INPUT0@', '@INPUT@', '@OUTDIR@']
)

patch_libv5rt = custom_target(
  'patch-libv5rt',
  input: [
    'patch-libv5rt.py',
  ],
  output: 'libv5.a',
  depends: libv5rt,
  command: [python, '@INPUT@', keep_object_files, '@OUTDIR@']
)

v5_dep = declare_dependency(
  sources: [patch_headers, patch_libv5rt]
)