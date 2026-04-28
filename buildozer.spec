[app]

# (str) Title of your application
title = TOMS TEST LAB

# (str) Package name
package.name = imagetest

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
# ДОБАВЛЕНО xml для file_paths.xml
source.include_exts = py,png,jpg,jpeg,kv,ttf,txt,db,xml

# (str) Application versioning
version = 0.1.1

# (list) Application requirements
requirements = python3, kivy==2.3.0, kivymd==1.1.1, pillow, plyer, pyjnius, android, sharedstorage4kivy, https://github.com/Android-for-Python/gestures4kivy/archive/main.zip, https://github.com/Android-for-Python/camera4kivy/archive/main.zip

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, MANAGE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
# ИСПРАВЛЕНО: используем 0 вместо False для совместимости с Python 3.12
android.skip_update = 0

# (bool) If True, then automatically accept SDK license
# ИСПРАВЛЕНО: используем 1 вместо True
android.accept_sdk_license = 1

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (list) Android application architectures
android.archs = arm64-v8a

# (bool) enables Android auto backup feature
android.allow_backup = 1

# --- СЕКЦИЯ ДЛЯ РАБОТЫ КАМЕРЫ И ГАЛЕРЕИ ---

# Связываем файл путей (должен лежать в res/xml/file_paths.xml)
android.add_xml = res/xml/file_paths.xml

# Настройка провайдера файлов
android.meta_data = androidx.core.content.FileProvider=android.support.v4.content.FileProvider

# Gradle зависимости для CameraX (РЕШАЕТ КРАШ ПРИ КАСАНИИ)
android.gradle_dependencies = "androidx.camera:camera-core:1.3.0", "androidx.camera:camera-camera2:1.3.0", "androidx.camera:camera-lifecycle:1.3.0", "androidx.camera:camera-video:1.3.0", "androidx.camera:camera-view:1.3.0", "androidx.camera:camera-extensions:1.3.0"

# ------------------------------------------

[buildozer]
log_level = 2
warn_on_root = 1
