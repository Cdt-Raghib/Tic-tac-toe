from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

class MySettings(Popup):
	instance = ObjectProperty()
	
	def __init__(self, inst, **kwargs):
		super().__init__(**kwargs)
		self.instance = inst

	def saveSettings(self, children, inst):
		for f in children:
			f.save(inst)
	