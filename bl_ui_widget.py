import gpu
import bgl

from gpu_extras.batch import batch_for_shader

class BL_UI_Widget:
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = (0.8, 0.8, 0.8, 1.0)
        self.update(self.x, self.y)
        
    def set_bg_color(self, color):
        self.bg_color = color
		    
    def draw(self):
        self.shader.bind()
        self.shader.uniform_float("color", self.bg_color)
        
        bgl.glEnable(bgl.GL_BLEND)
        self.batch_panel.draw(self.shader) 
        bgl.glDisable(bgl.GL_BLEND)
    
    def update(self, x, y):
        
        indices = ((0, 1, 2), (0, 2, 3))

        # bottom left, top left, top right, bottom right
        vertices = (
                    (self.x, self.y), 
                    (self.x, self.y+self.height), 
                    (self.x + self.width, self.y + self.height),
                    (self.x + self.width, self.y))
                    
        self.shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        self.batch_panel = batch_for_shader(self.shader, 'TRIS', {"pos" : vertices}, indices=indices)
    
    def handle_event(self, event):
        if(event.type == 'LEFTMOUSE'):
            if(event.value == 'PRESS'):
                return self.mouse_down(event.mouse_region_x, event.mouse_region_y)
            else:
                self.mouse_up(event.mouse_region_x, event.mouse_region_y)
                
        
        elif(event.type == 'MOUSEMOVE'):
            self.mouse_move(event.mouse_region_x, event.mouse_region_y)
            return False
                        
        return False                 


    def is_in_rect(self, x, y):
        
        if (
            (self.x <= x <= (self.x + self.width)) and 
            (self.y <= y <= (self.y + self.height))
            ):
            return True
           
        return False      

    def mouse_down(self, x, y):       
        return self.is_in_rect(x,y)

    def mouse_move(self, x, y):
        pass

    def mouse_up(self, x, y):
        pass