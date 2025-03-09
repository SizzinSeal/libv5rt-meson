project('v5rt', 'c')

cc = meson.get_compiler('c')
v5rt_dep = declare_dependency(
  dependencies : cc.find_library('v5rt', dirs : meson.current_source_dir()),
  include_directories : include_directories('include'))

meson.override_dependency('v5rt', v5rt_dep)
