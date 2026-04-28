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
    from android.permissions import request_permissions, Permission, check_permission
    
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    MediaStore = autoclass('android.provider.MediaStore')
    Uri = autoclass('android.net.Uri')
    File = autoclass('java.io.File')
    FileProvider = autoclass('androidx.core.content.FileProvider')
    
    try:
        from sharedstorage4kivy import SharedStorage
    except ImportError:
        SharedStorage = None

from plyer import filechooser

KV = '''
MDScreen:
    md_bg_color: 0.1, 0.1, 0.1, 1

    MDBoxLayout:
        orientation: 'vertical'
        padding: "10dp"
        spacing: "5dp"

        # Предпросмотр выбранного изображения
        FitImage:
            id: display_img
            source: "assets/placeholder.png"
            size_hint: None, None
            size: "220dp", "220dp"
            pos_hint: {"center_x": .5}
            radius: [20, ]

        MDLabel:
            id: status_label
            text: "Тестовый стенд: Камера и Галерея"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "Caption"
            adaptive_height: True

        # Скролл, чтобы все кнопки влезли на экран
        ScrollView:
            do_scroll_x: False
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                spacing: "12dp"
                padding: ["10dp", "10dp", "10dp", "20dp"]

                MDRaisedButton:
                    text: "📷 СДЕЛАТЬ ФОТО (Intent)"
                    size_hint_x: 1
                    md_bg_color: 0.2, 0.6, 0.2, 1
                    on_release: app.test_camera_intent()

                MDRaisedButton:
                    text: "1. SharedStorage (Copy to Cache)"
                    size_hint_x: 1
                    on_release: app.test_shared_storage()

                MDRaisedButton:
                    text: "2. Intent (GET_CONTENT) + Copy"
                    size_hint_x: 1
                    on_release: app.test_get_content()

                MDRaisedButton:
                    text: "3. Intent (ACTION_PICK) - No Copy"
                    size_hint_x: 1
                    on_release: app.test_action_pick()

                MDRaisedButton:
                    text: "4. Plyer Filechooser"
                    size_hint_x: 1
                    on_release: app.test_plyer_filechooser()
                    
                MDRaisedButton:
                    text: "5. Camera4Kivy (choose_file)"
                    size_hint_x: 1
                    on_release: app.test_camera4kivy()
                    
                MDFlatButton:
                    text: "ОЧИСТИТЬ КЭШ"
                    text_color: 1, 0.3, 0.3, 1
                    pos_hint: {"center_x": .5}
                    on_release: app.clear_local_files()
'''

class TestApp(MDApp):
    camera_path = StringProperty("")

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        # Запрос всех необходимых разрешений при запуске [cite: 56]
        if platform == 'android':
            request_permissions([
                Permission.CAMERA,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_MEDIA_IMAGES
            ])
            activity.bind(on_activity_result=self.on_android_result)

    def test_camera_intent(self):
        """Метод №6: Сделать фото и сохранить в папку приложения"""
        if platform == 'android':
            if not check_permission(Permission.CAMERA):
                self.root.ids.status_label.text = "Нет прав на камеру"
                return

            intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            filename = f"photo_{int(os.times().elapsed)}.jpg"
            save_path = os.path.join(self.user_data_dir, filename)
            self.camera_path = save_path
            
            photo_file = File(save_path)
            # Динамическое получение authority для FileProvider
            package_name = PythonActivity.mActivity.getPackageName()
            authority = f"{package_name}.fileprovider"
            
            uri = FileProvider.getUriForFile(PythonActivity.mActivity, authority, photo_file)
            intent.putExtra(MediaStore.EXTRA_OUTPUT, cast('android.os.Parcelable', uri))
            PythonActivity.mActivity.startActivityForResult(intent, 4000)

    def test_shared_storage(self):
        """Метод №1: Современный способ через sharedstorage4kivy"""
        if platform == 'android' and SharedStorage:
            try:
                ss = SharedStorage()
                path = ss.copy_from_shared('Images')
                if path:
                    final_path = self.copy_file_to_app_folder(path)
                    self.update_ui(final_path, "SharedStorage")
            except Exception as e:
                self.root.ids.status_label.text = f"SS Error: {e}"

    def test_get_content(self):
        """Метод №2: Выбор через системный Intent с копированием байтов"""
        if platform == 'android':
            intent = Intent(Intent.ACTION_GET_CONTENT).setType("image/*")
            PythonActivity.mActivity.startActivityForResult(intent, 2000)

    def test_action_pick(self):
        """Метод №3: Выбор из галереи без копирования (прямой URI)"""
        if platform == 'android':
            intent = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
            PythonActivity.mActivity.startActivityForResult(intent, 3000)

    def test_plyer_filechooser(self):
        """Метод №4: Классический Plyer"""
        filechooser.open_file(on_selection=lambda x: self.update_ui(x[0], "Plyer") if x else None)

    def test_camera4kivy(self):
        """Метод №5: Выбор файла через библиотеку Camera4Kivy"""
        if platform == 'android':
            try:
                from camera4kivy import Preview
                Preview().choose_file(on_selection=lambda x: self.update_ui(x, "C4K"))
            except Exception as e:
                self.root.ids.status_label.text = f"C4K Error: {e}"

    def on_android_result(self, requestCode, resultCode, intent):
        """Обработка ответов от всех системных окон Android"""
        if resultCode == -1: # RESULT_OK
            if requestCode == 4000: # Камера
                self.update_ui(self.camera_path, "Camera Capture")
            elif requestCode == 2000: # Галерея (копирование)
                if intent and intent.getData():
                    uri = intent.getData()
                    path = self.copy_uri_to_internal_storage(uri)
                    self.update_ui(path, "Intent (Copied)")
            elif requestCode == 3000: # Галерея (прямой URI)
                if intent and intent.getData():
                    uri = intent.getData()
                    self.update_ui(uri.toString(), "Intent (Direct URI)")

    def copy_uri_to_internal_storage(self, uri):
        """Ручное копирование данных из URI в файл приложения"""
        try:
            context = PythonActivity.mActivity
            filename = f"copy_{int(os.times().elapsed)}.jpg"
            dest_path = os.path.join(self.user_data_dir, filename)
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
        except Exception as e: return f"Error: {e}"

    def copy_file_to_app_folder(self, source_path):
        """Копирование существующего файла"""
        dest = os.path.join(self.user_data_dir, os.path.basename(source_path))
        shutil.copy2(source_path, dest)
        return dest

    def update_ui(self, path, method_name):
        """Обновление картинки и текста на экране"""
        if path:
            self.root.ids.display_img.source = path
            self.root.ids.display_img.reload()
            self.root.ids.status_label.text = f"Метод: {method_name}\nПуть: {path}"

    def clear_local_files(self):
        """Очистка всех созданных фото из папки приложения"""
        for f in os.listdir(self.user_data_dir):
            if f.endswith(".jpg") or f.endswith(".png"):
                os.remove(os.path.join(self.user_data_dir, f))
        self.root.ids.display_img.source = "assets/placeholder.png"
        self.root.ids.status_label.text = "Кэш очищен"

if __name__ == '__main__':
    TestApp().run()