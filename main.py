from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.utils import platform
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
import os
import shutil

# Системные импорты для Android
if platform == 'android':
    from jnius import autoclass, cast
    from android import activity
    from camera4kivy import Preview
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    MediaStore = autoclass('android.provider.MediaStore')
    Uri = autoclass('android.net.Uri')

KV = '''
MDScreen:
    md_bg_color: 0, 0, 0, 1

    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"

        FitImage:
            id: display_img
            source: "assets/placeholder.png"
            size_hint: None, None
            size: "200dp", "200dp"
            pos_hint: {"center_x": .5}
            radius: [20, ]

        MDLabel:
            id: status_label
            text: "Выберите метод теста"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDGridLayout:
            cols: 1
            spacing: "10dp"
            adaptive_height: True

            MDRaisedButton:
                text: "1. Camera4Kivy (choose_file)"
                size_hint_x: 1
                on_release: app.test_camera4kivy()

            MDRaisedButton:
                text: "2. Intent (GET_CONTENT)"
                size_hint_x: 1
                on_release: app.test_get_content()

            MDRaisedButton:
                text: "3. Intent (ACTION_PICK)"
                size_hint_x: 1
                on_release: app.test_action_pick()
'''

class TestApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_MEDIA_IMAGES
            ])
            # Привязываем слушателя для методов 2 и 3
            activity.bind(on_activity_result=self.on_android_result)

    # --- МЕТОД 1: Camera4Kivy ---
    def test_camera4kivy(self):
        if platform == 'android':
            try:
                Preview().choose_file(on_selection=self.update_ui)
            except Exception as e:
                self.root.ids.status_label.text = f"C4K Error: {e}"
        else:
            self.root.ids.status_label.text = "Работает только на Android"

    # --- МЕТОД 2: GET_CONTENT ---
    def test_get_content(self):
        if platform == 'android':
            intent = Intent(Intent.ACTION_GET_CONTENT)
            intent.setType("image/*")
            chooser = Intent.createChooser(intent, cast('java.lang.CharSequence', autoclass('java.lang.String')("Метод 2")))
            PythonActivity.mActivity.startActivityForResult(chooser, 2000)

    # --- МЕТОД 3: ACTION_PICK ---
    def test_action_pick(self):
        if platform == 'android':
            intent = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
            PythonActivity.mActivity.startActivityForResult(intent, 3000)

    def on_android_result(self, requestCode, resultCode, intent):
        if intent and (requestCode == 2000 or requestCode == 3000):
            uri = intent.getData()
            path = self.copy_uri_to_app(uri)
            self.update_ui(path)

    def copy_uri_to_app(self, uri):
        try:
            context = PythonActivity.mActivity
            dest_path = os.path.join(self.user_data_dir, "test_temp.jpg")
            input_stream = context.getContentResolver().openInputStream(uri)
            output_stream = autoclass('java.io.FileOutputStream')(dest_path)
            buffer = autoclass('java.lang.reflect.Array').newInstance(autoclass('java.lang.Byte').TYPE, 4096)
            while True:
                read = input_stream.read(buffer)
                if read == -1: break
                output_stream.write(buffer, 0, read)
            input_stream.close()
            output_stream.close()
            return dest_path
        except Exception as e:
            return f"Copy Error: {e}"

    def update_ui(self, path):
        if path and os.path.exists(path):
            self.root.ids.display_img.source = path
            self.root.ids.display_img.reload()
            self.root.ids.status_label.text = f"Успех! Путь: {path}"
        else:
            self.root.ids.status_label.text = f"Файл не найден: {path}"

if __name__ == '__main__':
    TestApp().run()