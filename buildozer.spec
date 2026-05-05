[app]

# (str) Title of your application
title = Image Test Lab

# (str) Package name
package.name = imagetest

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# Добавлены прямые ссылки на архивы для camera4kivy и gestures4kivy
requirements = python3, kivy==2.3.1, kivymd==1.1.1, pillow, pyjnius
# (str) Presplash of the application
presplash.filename = %(source.dir)s/assets/placeholder.png

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/placeholder.png

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# Максимальный набор прав для тестирования доступа к медиа
android.permissions = READ_EXTERNAL_STORAGE, READ_MEDIA_IMAGES, WRITE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) enables Android auto backup feature
android.allow_backup = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1