import cv2
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from numpy import right_shift
import omr_python
import omr_camera
import omr_input
import cam_func
import time
from plyer import filechooser
from kivy.core.window import Window
import time
import io
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import csv

questions = 10
choices = int()
ans_list = []


class MainWindow(Screen):
    pass
    def file_chooser(self):
        filechooser.open_file(on_selection=self.selected)
    def selected(self,selection):
        self.ids.selected_path.text = selection[0]
class TestWindow(Screen):
    pass

    def make_output(self):
        #img_path = self.ids.selected_path.text
        #marks = omr_python.omrfunc(img_path)
        
        print("in the window here")
    

    def file_chooser(self):
        filechooser.open_file(on_selection=self.selected)
    def selected(self,selection):
        if selection:
            self.ids.selected_path.text = selection[0]
            img_path = self.ids.selected_path.text

            questions = int(self.manager.get_screen("inputans").ids.number_of_questions.text)
            choices = int(self.manager.get_screen("inputans").ids.number_of_choices.text)
            ansstr = self.manager.get_screen("inputans").ids.correct_answers.text

            ans=[]
            for i in ansstr:
                j = int(i) - 1
                ans.append(j)

            val = omr_python.omrfunc(img_path,questions,choices,ans)
            self.ids.obtained_mark.text = "obtained mark is "+ str(val[1])
            img = val[0]
            buf1 = cv2.flip(img, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr') 
            #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.manager.get_screen("inputimgwindow").ids.inputimg.texture = texture1


            img = val[2]
            buf1 = cv2.flip(img, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr') 
            #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.manager.get_screen("detailed").ids.detailedimg.texture = texture1




class InputImgWindow(Screen):
    pass

    def update_win(self):
        print("updated...!")
        print(questions)
        self.ids.change_text.text = self.manager.get_screen("test").ids.obtained_mark.text
        self.ids.inputimg.source = "3.jpg"




class DetailedImgWindow(Screen):
    pass


class ResultWindow(Screen):
    print("result image window")
    pass

        

class ThirdWindow(Screen):
    pass

   
class WindowManager(ScreenManager):
    pass


class CameraClick(Screen):
    def __init__(self,**kwargs):
        super(CameraClick, self).__init__(**kwargs)
        Clock.schedule_interval(self.capture, 1/15)
    

    def capture(self,dt):
        if self.ids.switch.active:

            questions = int(self.manager.get_screen("inputans").ids.number_of_questions.text)
            choices = int(self.manager.get_screen("inputans").ids.number_of_choices.text)
            ansstr = self.manager.get_screen("inputans").ids.correct_answers.text

            ans=[]
            for i in ansstr:
                j = int(i) - 1
                ans.append(j)

            vid = False
            if self.ids.vidswitch.active: 
                vid = True
            else:
                vid == False

            img = omr_camera.onCamera(questions,choices,ans,vid)
            buf1 = cv2.flip(img, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr') 
            #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.ids.result_img.texture = texture1
        


class InputAnswers(Screen):
    pass





    def file_chooser(self):
        filechooser.open_file(on_selection=self.selected)
    def selected(self,selection):
        if selection:
            self.ids.selected_path.text = selection[0]
            img_path = self.ids.selected_path.text

            questions = int(self.manager.get_screen("inputans").ids.number_of_questions.text)
            choices = int(self.manager.get_screen("inputans").ids.number_of_choices.text)
            ansstr = self.manager.get_screen("inputans").ids.correct_answers.text

            ans=[]
            for i in ansstr:
                j = int(i) - 1
                ans.append(j)

            right_answers = omr_input.omrfunc(img_path,questions,choices)
            s=""
            for i in right_answers:
                s += str(i+1)
            self.ids.correct_answers.text = s
    
    def saveanswers(self):
        f = open("answers.csv", "w")
        questions = self.ids.number_of_questions.text
        choices = self.ids.number_of_choices.text
        ans = self.ids.correct_answers.text
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow([questions,choices,ans])
        f.close()


class InputCamera(Screen):
    pass

    def __init__(self,**kwargs):
        super(InputCamera, self).__init__(**kwargs)
        Clock.schedule_interval(self.capture, 1/15)
    
    img = cv2.imread("start_cam.png")

    def capture(self,dt):
        if self.ids.toggle.active:
            

            img = cam_func.onCamera()
            buf1 = cv2.flip(img, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr') 
            #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.ids.camera.texture = texture1

            questions = int(self.manager.get_screen("inputans").ids.number_of_questions.text)
            choices = int(self.manager.get_screen("inputans").ids.number_of_choices.text)
            ansstr = self.manager.get_screen("inputans").ids.correct_answers.text
            
            ans=[]
            for i in ansstr:
                j = int(i) - 1
                ans.append(j)

            val = cam_func.omrfunc(img,questions,choices,ans)
            self.manager.get_screen("test").ids.obtained_mark.text = "obtained mark is "+ str(val[1])
            img = val[0]
            buf1 = cv2.flip(img, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr') 
            #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.manager.get_screen("inputimgwindow").ids.inputimg.texture = texture1


            img = val[2]
            buf1 = cv2.flip(img, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr') 
            #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.manager.get_screen("detailed").ids.detailedimg.texture = texture1


    def cheese(self):

        self.ids.toggle.active = False







kv = Builder.load_file("my.kv")

class MyMainApp(App):
    def build(self):
        return kv
    


if __name__ == "__main__":
    MyMainApp().run()    
