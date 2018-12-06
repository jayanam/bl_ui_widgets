import bpy

from bpy.types import Operator
 
from . bl_ui_button import *
from . bl_ui_drag_panel import *
from . bl_ui_draw_op import *
    
class DP_OT_draw_operator(BL_UI_OT_draw_operator):
    
    bl_idname = "object.dp_ot_draw_operator"
    bl_label = "bl ui widgets custom operator"
    bl_description = "Demo operator for bl ui widgets" 
    bl_options = {'REGISTER'}
    	
    def __init__(self):
        
        super().__init__()
            
        self.panel = BL_UI_Drag_Panel(300,300,300,100)
        self.panel.set_bg_color((0.6, 0.8, 0.8, 0.6))
        
        self.button1 = BL_UI_Button(20, 20, 120, 30)
        self.button1.set_bg_color((0.2, 0.8, 0.8, 0.8))
        self.button1.set_mouse_down(self.button1_press)
        self.button1.set_text("Scale")
        
        self.button2 = BL_UI_Button(160, 20, 120, 30)
        self.button2.set_bg_color((0.2, 0.8, 0.8, 0.8))
        self.button2.set_mouse_down(self.button2_press)
        self.button2.set_text("Rotate")
        
        self.widgets = [self.panel, self.button1, self.button2]
        
        self.panel.add_widgets([self.button1, self.button2])
        
    
    # Button press handlers    
    def button1_press(self, widget):
        print("Button '{0}' is pressed".format(widget.text))
        active_obj = bpy.context.view_layer.objects.active
        if active_obj is not None:
            active_obj.scale = (1, 1, 2.0)
        
    def button2_press(self, widget):
        print("Button '{0}' is pressed".format(widget.text))
        active_obj = bpy.context.view_layer.objects.active
        if active_obj is not None:
            active_obj.rotation_euler = (0, 30, 90)