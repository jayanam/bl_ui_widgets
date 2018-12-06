from . bl_ui_widget import * 

class BL_UI_Drag_Panel(BL_UI_Widget):
    
    def __init__(self, x, y, width, height):
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.is_drag = False
        self.widgets = []
        super().__init__(x,y, width, height)
        
    def add_widgets(self, widgets):
        self.widgets = widgets
        self.layout_widgets()
        
    def layout_widgets(self):
        for widget in self.widgets:
            widget.update(self.x_screen + widget.x, self.y_screen + widget.y)   
    
    def update(self, x, y):
        super().update(x - self.drag_offset_x, y - self.drag_offset_y)
        

    def mouse_down(self, x, y):
        
        print("{0} x {1}".format(x,y))
        print("Screen {0} x {1}".format(self.x_screen,self.y_screen))
        
        if self.is_in_rect(x,y):
            print("In Rect!")
            self.is_drag = True
            self.drag_offset_x = x - self.x_screen
            self.drag_offset_y = y - self.y_screen
            return True
        
        return False

    def mouse_move(self, x, y):
        if self.is_drag:
            self.update(x, y)
            self.layout_widgets()

    def mouse_up(self, x, y):
        self.is_drag = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0