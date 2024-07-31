import kivy
from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
#from kivy.uix.settings import Settings
from functools import partial
import numpy as np
import time

from bingobox import BingoBox
from globvar import set #depricated

class GlobalVar:
	main_instance = ObjectProperty()

class NamedButt(Button):
	name = StringProperty()
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class Color:
    def rgba(self, ls:list):
        for f in ls:
            yield f/255.0
		
class UIBox(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.rows = 3
		self.cols = 3
		self.function = None
		
	def ffbind(self, __callable__):
		self.function = __callable__
	
	def call(self, dt):
		self.function(dt)
		
	def create(self, dim = 3):
		print(self.rows, self.cols)
		for f in range(dim*dim):
			self.add_widget(NamedButt(name = str(f), text='', on_press=self.call, font_size= '24dp'))
	
	def disable_all(self):
		for f in self.children:
			f.disabled = True
	
	def enable_all(self):
		for f in self.children:
			f.disabled = False
	
	def remove_all(self):
		print(self.children)
		for f in self.children[:]:
			self.remove_widget(f)
   	
	def reload_with_dim(self, side):
		self.remove_all()
		self.rows = side
		self.cols = side
		self.create(dim=side)

 
class  Box(FloatLayout):
	turn = 1
	x = UIBox()
	tic_matrix = np.zeros(9, int)
	dim = 3
	tic_checker = BingoBox(dim,dim)
	comment = StringProperty("Player 1's turn")
	color = ObjectProperty((0,1,0,1))
	_thread = None
	font = StringProperty('assets/fonts/10 Cent Soviet.ttf')
	settings_init = False
	bind_settings = ObjectProperty()
	symbol_set = ['O','X','.']
	color_set = [(0,1,0,1),tuple(Color().rgba([255,128,0,255])), tuple(Color().rgba([236,236,0,255]))]
	total_palyer = 2
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		#set(main_instance=id(self))
		print(type(self.x))
		self.x.pos_hint = {'center_x':0.5, 'center_y': 0.6}
		self.x.size_hint = (None,None)
		self.x.size = (300,300)
		self.x.ffbind(self.pressed)
		self.x.create()
		self.add_widget(self.x)
		self.tic_checker.assign(self.tic_matrix)		
		self.lb = Label(text = self.comment, size_hint= (None,None), size = ('200dp', '10dp'), pos_hint={'center_x':0.5, 'center_y':0.3}, color = self.color, font_size= '20dp', font_name=self.font)
		self.add_widget(self.lb)
		self._thread = Clock.create_trigger(self.refresh, 2)

	def openSettings(self, obj=None):
		if not self.settings_init:
			self.bind_settings = obj
			self.settings_init = True

		self.bind_settings.open()
  
	def change_turn(self):
		if self.turn == self.total_palyer:
			self.turn = 1
		else:
			self.turn += 1

		self.lb.color = self.color_set[self.turn-1]
		self.lb.text = f"Player {self.turn}'s turn"
		
	def reload_ui(self):
		print(self.dim)
		#self.x.size = (700,700)
		self.x.reload_with_dim(self.dim)
  
	def refresh(self, dt=None):
		l = len(self.x.children)
		for f in self.x.children:
			f.text = ''
		
		self.tic_checker.redim(self.dim,self.dim)
		self.tic_matrix = np.zeros(self.dim*self.dim, int)
		self.tic_checker.assign(self.tic_matrix)
		self.lb.text = "Player 1's turn"
		self.lb.color = (0,1,0,1)
		self.turn = 1
		self.x.enable_all()
		self._thread.cancel()
	
	def isfilled(self):
		for i in self.tic_matrix:
			if not i:
				return False
		
		return True
				
	def pressed(self, dt):
		if self.tic_matrix[int(dt.name)] != 0:
			return

		dt.text = self.symbol_set[self.turn-1]
		self.tic_matrix[int(dt.name)] = self.turn
		m = self.tic_checker.check_all(find=self.turn)
		if m>0:
			self.lb.text = f'Player {self.turn} won'
			self.x.disable_all()
			self._thread()
			return
		
		if self.isfilled():
			self.lb.text = 'Match drawn!'
			self.lb.color = (0,0,1,1)
			self._thread()
			return 
				
		self.change_turn()

#class MySetting(Settings):
#	def __init__(self, **kwargs):
#		super().__init__(**kwargs)
#		self.orientation = 'vertical'
#		self.set = Button(text = 'Settings')
#		self.add_widget(self.set)

Builder.load_file('box.kv')
class MainApp(App):
	def build(self):
		Window.clearcolor = (0,0,0,1)
		#self.create_settings()
		#self.app.display_settings()
		GlobalVar.main_instance = Box()
		return GlobalVar.main_instance

if __name__ == '__main__':
	MainApp().run()
	