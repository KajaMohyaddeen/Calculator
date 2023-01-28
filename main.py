from kivy.clock import Clock
from kivy.config import Config
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
import math

from kivy.uix.widget import Widget

Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '600')


class Btn(Button):
    def __init__(self, val='0', **kwargs):
        super(Btn, self).__init__(**kwargs)
        self.text = val


class MainLayout(FloatLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

    def prev(self):
        app = App.get_running_app()
        if len(app.history) != 0:
            app.val_str = app.history.pop()


class Keys(GridLayout):

    def __init__(self, **kwargs):
        super(Keys, self).__init__(**kwargs)
        self.cols = 4
        self.rows = 5
        self.add_keys()

    keys = ['AC', 'C', "%", '/', '7', '8', '9', '*', '4', '5', '6', '-', '1', '2', '3', '+', '( )', '0', '.', '=']

    def add_keys(self):
        for i in self.keys:
            self.add_widget(Btn(i))


class History(Widget):
    app = App.get_running_app()
    layout = GridLayout(cols=1, rows=4)

    def __init__(self, **kwargs):
        super(History, self).__init__(**kwargs)
        self.add_widget(self.layout)


class MyApp(App):
    val_str=StringProperty()
    history = ListProperty([])
    click = SoundLoader.load("click.wav")
    click.volume = 0.3
    flag = 0

    def do_operation(self, txt):

        if self.val_str == "Error" or self.val_str == "Zero-div":
            self.val_str = ""

        if txt == "AC":
            self.flag = 0
            self.save_history()
            self.val_str = ""

        elif txt == "C":
            self.flag = 0
            self.save_history()
            self.val_str = self.val_str[0:-1]

        elif txt == "( )":
            if self.flag == 0:
                self.val_str += '('
                self.flag = 1
            else:
                self.flag = 0
                self.val_str += ')'

        elif txt == "=":
            try:
                self.save_history()
                self.val_str = str(eval(self.val_str))
            except ZeroDivisionError:
                self.save_history()
                self.val_str = "Zero-div"
            except Exception:
                self.save_history()
                self.val_str = "Error"

        elif txt == "sqrt":
            if not self.val_str.isalpha():
                self.val_str = str(math.sqrt(float(self.val_str)))

        elif txt == "pow":
            if not self.val_str.isalpha():
                self.val_str = str(math.pow(round(float(self.val_str), 4), 2))

        elif txt == "abs":
            if not self.val_str.isalpha():
                self.val_str = str(abs(float(self.val_str)))

        elif txt == "floor":
            if not self.val_str.isalpha():
                self.val_str = str(math.floor(float(self.val_str)))

        elif txt == "ceil":
            if not self.val_str.isalpha():
                self.val_str = str(math.ceil(float(self.val_str)))

        else:
            self.val_str += txt

    def save_history(self):
        if self.val_str and len(self.history) < 20:
            if len(self.history) == 0:
                self.history.append(self.val_str)
            elif self.history[-1] != self.val_str:
                self.history.append(self.val_str)

    def build(self):
        kv = Builder.load_string("""

#:import hexc kivy.utils.get_color_from_hex 

<MainLayout>


MainLayout:

    id:base_layout    
    canvas.before:
        Color:
            rgba:hexc('#222433')#'#122030'
        Rectangle:
            size:self.size
            pos:self.pos
            
    GridLayout:     # This layout separates the keys panel and value panel.
    
        cols:1
        rows:3
        padding:dp(10),dp(15),dp(10),dp(10)
        spacing:dp(10)
        
        FloatLayout:    # Float layout for value panel
        
            canvas.before:
                Color:
                    rgba:(0,0,0,.5)
                    
                RoundedRectangle:
                    size:self.size
                    pos:self.pos
                    radius:[10]

            size_hint:.6,.2
            
            ScrollView:
                
                #pos_hint:{'center_x':.5,'center_y':.5}
                pos:self.parent.pos
                Label:
                    canvas.before:
                        Color:
                            rgba:(1,1,1,0)
                        Rectangle:
                            size:self.size
                            pos:self.pos
                         
                    id:value
                    text:app.val_str
                    padding: dp(10),dp(10)
                    size_hint_y: None
                    text_size: self.width,None
                    height: self.texture_size[1]
                    font_name:'Montserrat-SemiBold.ttf'
                    font_size:'50sp'
                   
                
            BoxLayout:
                            
                pos:self.parent.x+self.parent.width-self.width-dp(5),self.parent.y
                size_hint:.3,.15
                spacing:'10px'
                
                Button:
                    canvas.before:
                        Color:
                            rgba:(1,1,1,.2)
                        RoundedRectangle:
                            size:self.size
                            pos:self.pos
                            radius:[10]
                            
                    text:"Back"
                    background_normal:""
                    background_color:(0,0,0,0)
                    font_name:'OstrichSans-Heavy.otf'
                    outline_color:(0,0,0,1)
                    outline_width:'1px'
                    on_press:root.prev()
                
                Button:
                    canvas.before:
                        Color:
                            rgba:(1,1,1,.2)
                        RoundedRectangle:
                            size:self.size
                            pos:self.pos
                            radius:[10]
                            
                    text:str(len(app.history))+"/20"
                    outline_color:(0,0,0,1)
                    outline_width:'1px'
                    font_name:'OstrichSans-Heavy.otf'
                    background_normal:""
                    background_color:(0,0,0,0)
                    on_press:app.history = []
                    
        ScrollView:
            
            do_scroll_y:False
            do_scroll_x:True
            size_hint_y:.06
            bar_color: hexc('#ffb901')
            bar_width: 2
            
            BoxLayout:
                width: self.minimum_width
                size_hint_x:None
                spacing:dp(10)
                padding:dp(5)
                 
                Btn1:
                    text:','
                    font_size:'0px'
                    outline_width:'0px'
                    Image:
                        source:'comma.png'
                        size:self.parent.size
                        pos:self.parent.pos
                    
                Btn1:
                    text:'sqrt'
                Btn1:
                    text:'pow'
                Btn1:
                    text:'avg'
                Btn1:
                    text:'max'
                Btn1:
                    text:'min'
                Btn1:
                    text:'root'
                Btn1:
                    text:'floor'
                Btn1:
                    text:'ceil'
                Btn1:
                    text:'rnd'
                Btn1:
                    text:'abs' 
                    
        Keys:               # Grid layout keys panel.
        
            id:keys_panel
            canvas.before:
                Color:
                    rgba:(1,1,1,0)#hexc('#122035')
                RoundedRectangle:
                    size:self.size
                    pos:self.pos
                    radius:[20]
                                
            id:base_window
            spacing:dp(2)
            padding:dp(1)
            size_hint:1,.4
    
<Btn>:
    flag:0
    text:"0000"
    background_color:(0,0,0,0)
    background_normal:""
    font_name:'Montserrat-SemiBold.ttf'
    font_size:'23sp'
    clr:'#33354a'
    outline_color:(0,0,0,1)
    outline_width:'1px'
    
    canvas.before:
        Color:
            rgba:hexc(self.clr)
        RoundedRectangle:
            size:self.size
            pos:self.pos
            radius:[4]
            
    on_press:
        self.clr='#222433'
        app.click.play()
        app.do_operation(self.text)
     
    on_release:self.clr='#33354a'
            
<Btn1@Btn>:
    text:'func()'
    font_name:'OstrichSans-Heavy.otf'
    font_size:'20sp'
    size_hint_x:None
    
    outline_width:'1px'

        """)
        return kv


if __name__ == '__main__':
    MyApp().run()
