[app]

# (str) Title of your application
title = TOMS

# (str) Package name
package.name = toms

# (str) Package domain (needed for android packaging)
package.domain = org.toms.app

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,ttf,txt,db,xml [cite: 2033]

# (str) Application versioning
version = 0.1.0

# (list) Application requirements
# ДОБАВЛЕНО: sharedstorage4kivy и gestures4kivy для корректной работы библиотек
requirements = python3, kivy==2.3.0, kivymd==1.1.1, pillow, plyer, pyjnius, android, sharedstorage4kivy, https://github.com/Android-for-Python/gestures4kivy/archive/main.zip, https://github.com/Android-for-Python/camera4kivy/archive/main.zip [cite: 2033]

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, MANAGE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES [cite: 2034]

# (int) Target Android API
android.api = 33 [cite: 2035]

# (int) Minimum API
android.minapi = 21 [cite: 2036]

# (str) Android NDK version
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False [cite: 2037]

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True [cite: 2038]

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (list) Android application architectures
android.archs = arm64-v8a

# (bool) enables Android auto backup feature
android.allow_backup = True

# --- СЕКЦИЯ ИСПРАВЛЕНИЙ ДЛЯ КАМЕРЫ И ФАЙЛОВ ---

# (list) XML to include in the android manifest for FileProvider
# Это связывает созданный тобой файл res/xml/file_paths.xml с манифестом
android.add_xml = res/xml/file_paths.xml

# (str) The name of the FileProvider class
android.meta_data = androidx.core.content.FileProvider=android.support.v4.content.FileProvider

# (list) Gradle dependencies for CameraX (решает проблему ClassNotFoundException из логов)
android.gradle_dependencies = "androidx.camera:camera-core:1.3.0", "androidx.camera:camera-camera2:1.3.0", "androidx.camera:camera-lifecycle:1.3.0", "androidx.camera:camera-video:1.3.0", "androidx.camera:camera-view:1.3.0", "androidx.camera:camera-extensions:1.3.0"

# ----------------------------------------------

[buildozer]
log_level = 2
warn_on_root = 1
