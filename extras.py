from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ColorProperty
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle


class BackgroundLabel(Label):
    background_color = ColorProperty([1, 0, 0, 1])  # Default red

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=self.background_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect, background_color=self.update_color)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_color(self, instance, value):
        self.canvas.before[0].rgba = value
        
        
class VariableLabel(BoxLayout):
    max = NumericProperty()
    min = NumericProperty()
    value = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.display = BackgroundLabel(text = str(self.value), size_hint= (0.8, 1), background_color = get_color_from_hex('#afafaf'))
        self.changer = BoxLayout(orientation= 'vertical', size_hint =(0.2, 1))
        self.increase_button = Button(text='+',size_hint= (1, 0.5), on_press=self.increase)
        self.decrease_button = Button(text='-',size_hint= (1, 0.5), on_press = self.decrease)
        self.changer.add_widget(self.increase_button)
        self.changer.add_widget(self.decrease_button)
        self.add_widget(self.display)
        self.add_widget(self.changer)
        self.thread = Clock.schedule_once(self.update)
        
    def update(self, dt):
        self.display.text = str(self.value)
        
    
    def increase(self, dt):
        self.value += 1
        self.display.text = str(self.value)
        self.decrease_button.disabled = False
        if self.value == self.max:
            dt.disabled= True
    
    def decrease(self, dt):
        self.value -= 1
        self.display.text = str(self.value)
        self.increase_button.disabled = False
        if self.value == self.min:
            dt.disabled = True
        
        
        