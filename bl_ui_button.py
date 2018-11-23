from . bl_ui_widget import *

import blf

class BL_UI_Button(BL_UI_Widget):
    
    def __init__(self, x, y, width, height):
        self.text_color        = (0.0, 0.0, 0.0, 1.0)
        self.hover_bg_color    = (0.5, 0.5, 0.5, 1.0)
        self.select_bg_color   = (0.7, 0.7, 0.7, 1.0)
        
        self.text = "Button"
        self.text_size = 16
        self.__state = 0
        super().__init__(x, y, width, height)
    
    # Will be supported in the next version
    def set_text_color(self, color):
        self.text_color = color
    
    def set_text(self, text):
        self.text = text
            
    def set_text_size(self, size):
        self.text_size = size
        
    def set_hover_bg_color(self, color):
        self.hover_bg_color = color
        
    def set_select_bg_color(self, color):
        self.select_bg_color = color
        
    def draw(self):
        self.shader.bind()
        
        color = self.bg_color
        text_color = self.text_color
        
        # pressed
        if self.__state == 1:
            color = self.select_bg_color

        # hover
        elif self.__state == 2:
            color = self.hover_bg_color
            
        self.shader.uniform_float("color", color)
        
        bgl.glEnable(bgl.GL_BLEND)
        self.batch_panel.draw(self.shader) 
        bgl.glDisable(bgl.GL_BLEND)      
        
        # Draw text
        blf.size(0, self.text_size, 72)
        size = blf.dimensions(0, self.text)
              
        blf.position(0, self.x + (self.width - size[0]) / 2.0, self.y + (self.height - size[1]) / 2.0, 0)
            
        blf.draw(0, self.text)
        
    def update(self, x, y):        
        super().update(x, y)
        
    def set_mouse_down(self, mouse_down_func):
        self.mouse_down_func = mouse_down_func   
                 
    def mouse_down(self, x, y):       
        if self.is_in_rect(x,y):
            self.__state = 1
            if(self.mouse_down_func is not None):
                self.mouse_down_func(self)            
                
            return True
        
        return False
    
    def mouse_move(self, x, y):
        if self.is_in_rect(x,y):
            if(self.__state != 1):
                
                # hover state
                self.__state = 2
        else:
            self.__state = 0
 
    def mouse_up(self, x, y):
        if self.is_in_rect(x,y):
            self.__state = 2
        else:
            self.__state = 0