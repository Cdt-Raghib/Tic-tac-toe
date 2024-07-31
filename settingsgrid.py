from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder

Builder.load_file('kivy/settingsgrid.kv')
class GridSettings(GridLayout):
    def save(self, inst):
        #inst is the main instance i.e. Box object
        if self.ids.dimension.text[0] == '1':
            dim = int(self.ids.dimension.text[:2])
        
        else:
            dim = int(self.ids.dimension.text[0])
        
        if dim!=inst.dim:
            inst.dim = dim
            inst.refresh()
            inst.reload_ui()
            
            inst.tic_checker.match_consecutive(inst.dim)