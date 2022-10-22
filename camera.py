from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time


Builder.load_file("cam.kv")


class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("test.png".format(timestr))
        print("Captured")


class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()