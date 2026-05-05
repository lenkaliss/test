import os
import io
import time
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import mainthread
from kivy.core.image import Image as CoreImage
from kivymd.app import MDApp
from kivy.logger import Logger

# Нативные импорты
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from jnius import autoclass
    from android import activity
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    FileOutputStream = autoclass('java.io.FileOutputStream')

KV = '''
MDBoxLayout:
    orientation: 'vertical'
    
    MDTopAppBar:
        title: "Image Render Test Lab"
        elevation: 4

    ScrollView:
        MDGridLayout:
            cols: 1
            adaptive_height: True
            padding: dp(15)
            spacing: dp(20)

            # СПОСОБ 1: ПРЯМОЕ КОПИРОВАНИЕ ПОТОКА
            MDCard:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(250)
                padding: dp(10)
                MDLabel:
                    text: "1. Native Stream Copy (File)"
                    bold: True
                    adaptive_height: True
                Image:
                    id: img_method_1
                    source: ''
                MDRaisedButton:
                    text: "Выбрать (Stream)"
                    on_release: app.open_gallery(method=1)

            # СПОСОБ 2: CORE IMAGE (IN-MEMORY)
            MDCard:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(250)
                padding: dp(10)
                MDLabel:
                    text: "2. CoreImage (Bytes/Buffer)"
                    bold: True
                    adaptive_height: True
                Image:
                    id: img_method_2
                MDRaisedButton:
                    text: "Выбрать (Buffer)"
                    on_release: app.open_gallery(method=2)

            # СПОСОБ 3: ПРЯМОЙ ПУТЬ (ДЛЯ ПРОВЕРКИ ОШИБОК ДОСТУПА)
            MDCard:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(250)
                padding: dp(10)
                MDLabel:
                    text: "3. Direct Path (RealPath)"
                    bold: True
                    adaptive_height: True
                Image:
                    id: img_method_3
                MDRaisedButton:
                    text: "Выбрать (Direct Path)"
                    on_release: app.open_gallery(method=3)
'''

class ImageTestApp(MDApp):
    current_method = 1

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        if platform == 'android':
            request_permissions([
                Permission.READ_MEDIA_IMAGES,
                Permission.READ_EXTERNAL_STORAGE
            ])
            activity.bind(on_activity_result=self.on_handle_activity_result)

    def open_gallery(self, method):
        self.current_method = method
        if platform == 'android':
            intent = Intent(Intent.ACTION_GET_CONTENT)
            intent.setType("image/*")
            PythonActivity.mActivity.startActivityForResult(intent, 101)
        else:
            print("Тест доступен только на Android")

    @mainthread
    def on_handle_activity_result(self, request_code, result_code, data):
        if request_code == 101 and result_code == -1:
            uri = data.getData()
            if self.current_method == 1:
                self.method_stream_copy(uri)
            elif self.current_method == 2:
                self.method_core_image(uri)
            elif self.current_method == 3:
                self.method_direct_path(uri)

    # --- МЕТОД 1: Копирование в файл приложения ---
    def method_stream_copy(self, uri):
        try:
            cr = PythonActivity.mActivity.getContentResolver()
            path = os.path.join(self.user_data_dir, "method1.jpg")
            
            in_stream = cr.openInputStream(uri)
            out_stream = FileOutputStream(path)
            
            # Стандартный буфер
            buffer = bytearray(1024 * 64)
            while True:
                read = in_stream.read(buffer)
                if read == -1: break
                out_stream.write(buffer[:read])
            
            in_stream.close()
            out_stream.close()
            
            self.root.ids.img_method_1.source = path
            self.root.ids.img_method_1.reload()
        except Exception as e:
            Logger.error(f"Method 1 Error: {e}")

    # --- МЕТОД 2: Загрузка в память без сохранения на диск ---
    def method_core_image(self, uri):
        try:
            cr = PythonActivity.mActivity.getContentResolver()
            in_stream = cr.openInputStream(uri)
            
            # Читаем все байты сразу
            from jnius import cast
            # Используем вспомогательный метод для чтения всех байтов
            # В Python это проще сделать через цикл, как выше, но в BytesIO
            data_io = io.BytesIO()
            buffer = bytearray(1024 * 64)
            while True:
                read = in_stream.read(buffer)
                if read == -1: break
                data_io.write(buffer[:read])
            in_stream.close()
            
            data_io.seek(0)
            # Создаем текстуру из байтов
            core_img = CoreImage(data_io, ext="jpg")
            self.root.ids.img_method_2.texture = core_img.texture
        except Exception as e:
            Logger.error(f"Method 2 Error: {e}")

    # --- МЕТОД 3: Попытка взять реальный путь (обычно выдает ошибку доступа на Android 11+) ---
    def method_direct_path(self, uri):
        # На новых Android URI выглядит как content://... и через os.path.exists не читается
        # Этот метод покажет, почему "простой" способ не работает
        uri_string = uri.toString()
        try:
            # Пытаемся подсунуть URI напрямую в Image
            self.root.ids.img_method_3.source = uri_string
        except Exception as e:
            Logger.error(f"Method 3 Error: {e}")

if __name__ == '__main__':
    ImageTestApp().run()