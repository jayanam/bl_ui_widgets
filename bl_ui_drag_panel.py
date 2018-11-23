from . bl_ui_widget import * 

class BL_UI_Drag_Panel(BL_UI_Widget):
    
    def __init__(self, x, y, width, height):
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.is_drag = False
        super().__init__(x,y, width, height)

    
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