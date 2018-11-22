import gpu
import bgl

from gpu_extras.batch import batch_for_shader

class Drag_Panel:
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.is_drag = False
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.update(self.x, self.y)
        
    def set_color(self, color):
        self.color = color
    
    def draw(self):
        self.shader.bind()
        self.shader.uniform_float("color", self.color)
        
        bgl.glEnable(bgl.GL_BLEND)
        self.batch_panel.draw(self.shader) 
        bgl.glDisable(bgl.GL_BLEND)
    
    def update(self, x, y):
        
        indices = ((0, 1, 2), (0, 2, 3))
        
        self.x = x - self.drag_offset_x
        self.y = y - self.drag_offset_y
        
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
            return True
                        
        return False                 


    def is_in_rect(self, x, y):
        
        if (
            (self.x <= x <= (self.x + self.width)) and 
            (self.y <= y <= (self.y + self.height))
            ):
            return True
           
        return False      

    def mouse_down(self, x, y):
        
        if self.is_in_rect(x,y):
            self.is_drag = True
            self.drag_offset_x = x - self.x
            self.drag_offset_y = y - self.y
            return True
        
        return False

    def mouse_move(self, x, y):
        if self.is_drag:
            self.update(x, y)

    def mouse_up(self, x, y):
        self.is_drag = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0