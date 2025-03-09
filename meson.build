project('v5rt', 'c')

inc = include_directories('include')
v5rt = shared_library('simple',
  'simple.c',
  include_directories : inc,
  install : true)

v5rt_dep = declare_dependency(include_directories : inc,
  link_with : v5rt)
