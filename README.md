# Known Issues
- Printing too much output can cause running out of memory, should switch to subprocess.Popen() and set a maximum size limit 
for stdout that is dynamic to number of test cases

- ASTCheck and PEP8 functions show too much information in stacktrace, should use traceback to change the limit.
    - Fixed with custom grader, no traceback is shown.

- Importing can fail if the file name has '-' in it. Switch to using import lib to dynamically load

- Can access the PYC files from __pycache__ directory and leak the test data that way. 
    - *** Fixed with custom grader as the testbench python file is no longer imported by ed-grader.py

<!-- - Expected return code checking -->
<!-- 
- json parsing bug when missing name or score or something -->

-add @debug_expected_fail() decorator
- switch timeout to use subprocess.run(timeout = xxx ) instead of having it in the subprocess script

# Edstem

['rats', 'pkgconfig', 'vnc', 'edk2-armvirt', 'gdm', 'haskell-colour', 'gtk-3.0', 'haskell-wai-cors', 'xyzservices', 'readline', 'alsa-card-profile', 'liblouis', 'clang-doc', 'common-lisp', 'mysql', 'gnome-bluetooth', 'qemu', 'libdrm', 'prte', 'tek2plot', 'xdg-desktop-portal', 'mono-2.0', 'givaro', 'gitweb', 'glib-2.0', 'libmysofa', 'gnupg', 'gmt', 'dbus-1', 'tachyon', 'audit-rules', 'egl', 'qt', 'fontconfig', 'hwdata', 'cowsay', 'icu', 'xtables', 'fltk', 'GraphicsMagick-1.3.45', 'file', 'libthai', 'sundials', 'afl', 'wayland-eglstream', 'scan-view', 'ncat', 'texinfo', 'imlib2', 'gnome-shell', 'hspell', 'ppl', 'zsh', 'aclocal', 'nmap', 'pixmaps', 'openmpi', 'metainfo', 'avahi', 'source-highlight', 'screen', 'p11-kit', 'haskell-pandoc', 'gdb', 'automake-1.18', 'wireplumber', 'gnome-settings-daemon', 'R', 'opt-viewer', 'fish', 'hadoop', 'figlet', 'boostbook', 'openal', 'gettext', 'wayland-sessions', 'dict', 'awk', 'texmf-dist', 'gtk-doc', 'glade', 'gnuplot', 'daxctl', 'brltty', 'swig', 'iso-codes', 'threejs-sage', 'locale', 'git-gui', 'licenses', 'cmake', 'vr_actions', 'glvnd', 'GConf', 'kotlin', 'fig2dev', 'haskell-hscolour', 'ode', 'libgweather-4', 'cracklib', 'gstreamer-1.0', 'doc', 'cogl', 'dotnet', 'verilator', 'util-macros', 'icons', 'gcc-15.1.1', 'podofo', 'xfce4', 'aclocal-1.18', 'octave', 'autoconf', 'mathjax', 'emacs', 'alex', 'apr-1', 'xsessions', 'julia', 'zoneinfo-posix', 'ibus', 'openxr', 'bison', 'lv2specgen', 'desktop-directories', 'lua', 'm17n', 'vim', 'i18n', 'kbd', 'budgie', 'eigen3', 'haskell-pretty-show', 'ant', 'systemd', 'dateutils', 'perl5', 'libwacom', 'ovmf', 'mesa-demos', 'qt6', 'xfburn', 'info', 'wayland', 'applications', 'et', 'gdal', 'wayland-protocols', 'iml', 'clang', 'git-core', 'ghostscript', 'scala', 'mobile-broadband-provider-info', 'iana-etc', 'ss', 'clojure', 'empty.sshd', 'libtool', 'gitk', 'budgie-control-center', 'gvfs', 'dart-sass', 'inkscape', 'keyutils', 'slsh', 'lrcalc', 'ladspa', 'backgrounds', 'OVMF', 'libgedit-gtksourceview-300', 'evince', 'netpbm', 'gimp', 'drirc.d', 'defaults', 'edk2', 'sounds', 'singular', 'python-httpx', 'colord', 'haskell-doclayout', 'pic2plot', 'ellcurves', 'WebP', 'factory', 'fonts', 'libcaca', 'bash-completion', 'pmix', 'xfwm4', 'spa-0.2', 'enchant-2', 'pipewire', 'mime', 'fplll', 'mdadm', 'radare2', 'racket', 'parole', 'xr_actions', 'sympow', 'gtk-2.0', 'ca-certificates', 'reflexive_polytopes', 'texmf', 'tabset', 'thumbnailers', 'py4j', 'yosys', 'poppler', 'help', 'haskell-doctemplates', 'misc', 'zoneinfo-leaps', 'boost_predef', 'git', 'arrow', 'nim', 'graphite2', 'proj', 'opencv4', 'd', 'budgie-session', 'iproute2', 'bazel', 'glusterfs', 'Thunar', 'clutter-1.0', 'sbcl-source', 'polkit-1', 'gtkwave-gtk3', 'gir-1.0', 'cliquer', 'tc', 'X11', 'zoneinfo', 'haskell-happy-lib', 'gtksourceview-4', 'xcb', 'jupyter', 'gst-plugins-base', 'vala', 'libgpg-error', 'gedit', 'nano', 'model', 'ImageMagick-7', 'soundfonts', 'graphs', 'hwloc', 'zmq', 'gcc-arm-none-eabi', 'edk2-ovmf', 'file-roller', 'accountsservice', 'pari', 'xml', 'maxima', 'scan-build', 'gnome-control-center', 'installed-tests', 'scala3', 'xkeyboard-config-2', 'AAVMF', 'ffmpeg', 'pstoedit', 'lksctp-tools', 'gap', 'groff', '.mono', 'hlint', 'gnome-session', 'pacman', 'themes', 'libgnomekbd', 'terminfo', 'ucx', 'libinput', 'libalpm', 'djvu', 'gettext-0.25', 'tlpkg', 'udunits', 'subversion', 'ml_python', 'guile', 'graphviz', 'color', 'alsa', 'postgresql', 'ml_singular', 'cremona', 'haskell', 'man', 'makepkg-template', 'sbt', 'appstream', 'nltk_data', 'grpc', 'appdata', 'b2', 'java', 'gtk-4.0', 'iptables', 'libplot', 'makepkg', 'texi2any']\n



['mnt', 'run', 'tmp', '.dockerenv', 'opt', 'var', 'root', 'lib', 'boot', 'course', 'sbin', 'dev', 'home', 'lib64', 'usr', 'sys', 'proc', 'build', 'bin', 'services', 'etc', 'srv']\n


100mB file size limit in total for grader
20mB limit on student file workspace