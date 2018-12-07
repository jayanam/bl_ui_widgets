from . bl_ui_widget import *

import blf

class BL_UI_Slider(BL_UI_Widget):
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.text_color        = (0.0, 0.0, 0.0, 1.0)
        self.color          = (0.5, 0.5, 0.7, 1.0)
        self.hover_color    = (0.5, 0.5, 0.8, 1.0)
        self.select_color   = (0.7, 0.7, 0.7, 1.0)

        self.min = 0
        self.max = 100
        self.tickcount = 10
        
        self.text_size = 14
        self.__state = 0
        self.__is_drag = False
        self.__slider_pos = 0
        self.__slider_value = 0
        self.__slider_width = 5
        self.__slider_height = 13
        self.update(x, y)

    
    # Will be supported in the next version
    def set_text_color(self, color):
        self.text_color = color
            
    def set_text_size(self, size):
        self.text_size = size

    def set_color(self, color):
        self.color = color

    def set_hover_color(self, color):
        self.hover_color = color
        
    def set_select_color(self, color):
        self.select_color = color
                
    def draw(self):
        self.shader.bind()
        
        color = self.color
        text_color = self.text_color
        
        # pressed
        if self.__state == 1:
            color = self.select_color

        # hover
        elif self.__state == 2:
            color = self.hover_color
            
        self.shader.uniform_float("color", color)
        
        bgl.glEnable(bgl.GL_BLEND)
        self.batch_slider.draw(self.shader) 
        bgl.glDisable(bgl.GL_BLEND)      
        
        # Draw text
        sValue = str(self.__slider_value)
        blf.size(0, self.text_size, 72)
        size = blf.dimensions(0, sValue)
                      
        blf.position(0, self.__slider_pos + 1 + self.x_screen - size[0] / 2.0, 
                        self.y_screen + self.__slider_height + 5, 0)
            
        blf.draw(0, sValue)
        
    def update(self, x, y):  
        
        # Min                      Max
        #  |---------V--------------|
        
        self.x_screen = x
        self.y_screen = y
        
        # Slider triangles
        # 
        #        0
        #     1 /\ 2
        #      |  |
        #     3---- 4
        
        h = self.__slider_height
        w = self.__slider_width
        pos_y = self.y_screen + self.__slider_height
        pos_x = self.x_screen + self.__slider_pos
        
        indices = ((0, 1, 2), (1, 2, 3), (3, 2, 4))
        
        vertices = (
                    (pos_x    , pos_y    ),
                    (pos_x - w, pos_y - w),
                    (pos_x + w, pos_y - w),
                    (pos_x - w, pos_y - h),
                    (pos_x + w, pos_y - h)
                   )
                    
        self.shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        self.batch_slider = batch_for_shader(self.shader, 'TRIS', {"pos" : vertices}, indices=indices)

        
    def set_value_change(self, value_change_func):
        self.value_change_func = value_change_func
    
    def is_in_rect(self, x, y):
        if (
            (self.x_screen + self.__slider_pos - self.__slider_width <= x <= 
            (self.x_screen + self.__slider_pos + self.__slider_width)) and 
            (self.y_screen <= y <= (self.y_screen + self.__slider_height))
            ):
            return True
           
        return False

    def __value_to_pos(self, value):
        return self.width * value / (self.max - self.min)

    def __pos_to_value(self, pos):
        return int((self.max - self.min) * self.__slider_pos / self.width)

    def set_slider_value(self, value):
        if value < self.min:
            value = self.min
        if value > self.max:
            value = self.max

        if value != self.__slider_value:
            self.__slider_value = value

            try:
                self.value_change_func(self, self.__slider_value)
            except:
                pass

            self.__slider_pos = self.__value_to_pos(self.__slider_value)

    def __set_slider_pos(self, x):
        if x <= self.x_screen:
            self.__slider_pos = 0
        elif x >= self.x_screen + self.width:
            self.__slider_pos = self.width
        else:
            self.__slider_pos = x - self.x_screen

        newValue = self.__pos_to_value(self.__slider_pos)

        if newValue != self.__slider_value:
            self.__slider_value = newValue

            try:
                self.value_change_func(self, self.__slider_value)
            except:
                pass
                 
    def mouse_down(self, x, y):    
        if self.is_in_rect(x,y):
            self.__state = 1
            self.__is_drag = True
                
            return True
        
        return False
    
    def mouse_move(self, x, y):
        if self.is_in_rect(x,y):
            if(self.__state != 1):
                
                # hover state
                self.__state = 2
        else:
            self.__state = 0
        
        if self.__is_drag:
            self.__set_slider_pos(x)
            self.update(self.x_screen, self.y_screen)
 
    def mouse_up(self, x, y):
        self.__state = 0
        self.__is_drag = False