from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.properties import StringProperty,ObjectProperty
from kivy.uix.label import Label
from kivy.factory import Factory

import os

#from globvar import main_instance

class InstCheckBox(CheckBox):
	func = ObjectProperty()
	name = StringProperty()
	target = ObjectProperty()
	
	def __init__(self, bind, name='', **kwargs):
		super().__init__(**kwargs)
		self.name = name
		self.bind(active=bind)
		
class SetStyle(GridLayout):
	selected = StringProperty()
	target = ObjectProperty()
	default = '10 Cent Soviet.ttf'
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 2
		self.styles = os.listdir('assets/fonts')
		for f in self.styles:
			self.add_widget(InstCheckBox(name=f,group='style', bind=self.change, size_hint_x=0.2, state='down' if (self.default==f) else 'normal'))
			self.add_widget(Label(text=f, size_hint_x=0.8))
	
	def change(self, inst, value):
		print(value, inst)
		if value:
			self.selected = f'assets/fonts/{inst.name}'
			print(f'Selection: {self.selected}')

	def save(self, inst):
		print('Main instance from settings', inst)
		if self.selected == '':
			return
		if self.selected != "assets/fonts/Action Men.ttf":
			inst.lb.font_name = self.selected
		for f in inst.x.children:
			f.font_name = self.selected
   
		print('Font ', inst.font)