from kivy.clock import Clock
from kivy.config import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from jnius import autoclass
import math

Config.set('graphics','width','300')
Config.set('graphics','height','500')

class Btn(Button):
    def __init__(self,val='0',**kwargs):
        super(Btn,self).__init__(**kwargs)
        self.text = val
  
class MainLayout(FloatLayout):
    
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

    def prev(self):
        app = App.get_running_app()
        if len(app.history) != 0:
            app.str = app.history.pop()

class Keys(GridLayout):
    
    def __init__(self, **kwargs):
        super(Keys, self).__init__(**kwargs)
        self.cols = 4
        self.rows = 5
        Clock.schedule_once(lambda dt: self.add_keys(), 0)

    keys = ['AC', 'C', '%', '/', '7', '8', '9', '*', '4', '5', '6', '-', '1', '2', '3', '+', '( )', '0', '.', '=']

    def add_keys(self):
        for i in self.keys:
            self.add_widget(Btn(i))

class MyApp(App):

    str = StringProperty('')
    history = ListProperty([])
    flag = 0
    
    def do_operation(self,txt):

        if self.str == "Error" or self.str == "Zero-div":
            self.str = ""
            
        if txt == "AC":
            self.flag = 0
            self.save_history()
            self.str = ""
            
        elif txt =="C":
            self.flag = 0             
            self.save_history()
            self.str = self.str[0:-1]
                
        elif txt =="( )":
            if self.flag == 0:
                self.str += '('
                self.flag=1
            else:
                self.flag=0
                self.str += ')'
                
        elif txt =="=":
            try:
                self.save_history()
                self.str = str(eval(self.str))
            except ZeroDivisionError:
                self.save_history()
                self.str = "Zero-div"
            except Exception :
                self.save_history()
                self.str = "Error"
                
        elif txt == "sqrt":
            if not self.str.isalpha():
                self.str = str(math.sqrt(float(self.str)))
            
        elif txt == "pow":
            if not self.str.isalpha() :
                self.str = str(math.pow(round(float(self.str),4),2))
            
        elif txt == "abs":
            if not self.str.isalpha():
                self.str = str(abs(float(self.str)))
            
        elif txt == "floor":
            if not self.str.isalpha():
                self.str = str(math.floor(float(self.str)))
                    
        elif txt == "ceil":
            if not self.str.isalpha():
                self.str = str(math.ceil(float(self.str)))
            
        else:
            self.str += txt

    def save_history(self):
        if self.str and len(self.history)<20:
            if len(self.history) == 0 :
                self.history.append(self.str)
            elif self.history[-1]!=self.str:
                self.history.append(self.str)

    def build(self):
        kv = Builder.load_string("""

#:import hexc kivy.utils.get_color_from_hex 

<MainLayout>

MainLayout:
    
    id:base_layout    
    canvas.before:
        Color:
            rgba:hexc('#122030')
        Rectangle:
            size:self.size
            pos:self.pos
            
    GridLayout:     # This layout separates the keys panel and value panel.
    
        cols:1
        rows:3
        padding:dp(10),dp(30),dp(10),dp(10)
        spacing:dp(10)
        
        FloatLayout:    # Float layout for value panel
        
            canvas.before:
                Color:
                    rgba:(0,0,0,.5)
                    
                RoundedRectangle:
                    size:self.size
                    pos:self.pos
                    radius:[20]

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
                    text:app.str
                    padding: dp(10),dp(10)
                    size_hint_y: None
                    text_size: self.width,None
                    height: self.texture_size[1]
                    font_name:'ostrich-regular.ttf'
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
            bar_color: (0,0,0, 1)
            bar_width: 5
            
            BoxLayout:
                width: self.minimum_width
                size_hint_x:None
                spacing:dp(10)
                padding:dp(5)
                 
                Btn1:
                    text:','
                    font_size:'0px'
                    outline_width:'0px'
                    canvas.before:
                        Color:
                            rgba:1,1,1,.5
                        Rectangle:
                            source:'comma.png'
                            size:self.size
                            pos:self.pos
                        
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
            spacing:dp(1)
            padding:dp(1)
            size_hint:1,.4
    
<Btn>:
    flag:0
    text:"0000"
    background_color:(0,0,0,0)
    background_normal:""
    font_name:'ostrich-regular.ttf'
    font_size:'30sp'
    clr:(0,0,0,0)
    outline_color:(0,0,0,1)
    outline_width:'3px'
    
    canvas.before:
        Color:
            rgba:self.clr
        RoundedRectangle:
            size:self.size
            pos:self.pos
            radius:[30]
            
    on_press:
        self.clr=(0,0,0,0.5)
        app.do_operation(self.text)
     
    on_release:self.clr=(0,0,0,0)
            
<Btn1@Btn>:
    text:'func()'
    font_name:'OstrichSans-Heavy.otf'
    font_size:'20sp'
    size_hint_x:None
    width:dp(60)
    outline_width:'8px'

        """)
        return kv


if __name__ == '__main__':
    MyApp().run()