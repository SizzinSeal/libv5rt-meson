project('v5', 'c',
    version: '1.0',
)

# normally these would be the only 2 things you need to change if there is a new SDK version available.
version = 'V5_20240802_15_00_00' # the zipfile name, which also indicates the version
hash = '51fc8695402dd39d5713d20bda5d23699e85913d595e47cd550112ec290730a2' # sha256 of the zip, to verify it downloaded successfully

keep_object_files = [
  'v5_util.c.obj',
  'v5_apijump.c.obj',
  'v5_apiuser.c.obj',
  'v5_apigraphics.c.obj',
  'v5_apiversions.c.obj'
]

python = find_program('python3')
strip = find_program('arm-none-eabi-strip')

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
  command: [python, '@INPUT0@', '@INPUT@', '@OUTDIR@'],
  build_by_default: true,
)

strip_libv5rt = custom_target(
  'strip-libv5rt',
  input: 'libv5rt-strip-options.txt',
  output: 'libv5rt-stripped.a',
  depends: libv5rt,
  command: [ python, files('strip_wrapper.py'), strip, 'libv5rt.a', '@INPUT1@', '@OUTPUT@', '@OUTDIR@', ]
)

patch_libv5rt = custom_target(
  'patch-libv5rt',
  input: [
    'patch-libv5rt.py',
  ],
  output: 'libv5.a',
  depends: strip_libv5rt,
  command: [python, '@INPUT@', keep_object_files, '@OUTDIR@'],
  build_by_default: true,
)

v5_lib_dep = declare_dependency(
  sources: patch_libv5rt
)

v5_header_dep = declare_dependency(
  sources: patch_headers
)