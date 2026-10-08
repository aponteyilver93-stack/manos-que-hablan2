[app]
title = Manos que hablan
package.name = manosquehablan
package.domain = org.manos
source.dir = .
source.include_exts = py,png,jpg,kv,json
source.exclude_dirs = .github
version = 0.1
requirements = python3,kivy==2.3.0
orientation = portrait
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
