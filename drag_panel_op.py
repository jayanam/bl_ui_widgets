import bpy

from bpy.types import Operator
 
from . bl_ui_button import *
from . bl_ui_slider import *
from . bl_ui_drag_panel import *
from . bl_ui_draw_op import *
    
class DP_OT_draw_operator(BL_UI_OT_draw_operator):
    
    bl_idname = "object.dp_ot_draw_operator"
    bl_label = "bl ui widgets custom operator"
    bl_description = "Demo operator for bl ui widgets" 
    bl_options = {'REGISTER'}
    	
    def __init__(self):
        
        super().__init__()
            
        self.panel = BL_UI_Drag_Panel(300,300,300,130)
        self.panel.set_bg_color((0.8, 0.8, 0.8, 0.3))
        
        self.button1 = BL_UI_Button(20, 80, 120, 30)
        self.button1.set_bg_color((0.2, 0.8, 0.8, 0.8))
        self.button1.set_mouse_down(self.button1_press)
        self.button1.set_text("Scale")
        
        self.button2 = BL_UI_Button(160, 80, 120, 30)
        self.button2.set_bg_color((0.2, 0.8, 0.8, 0.8))
        self.button2.set_mouse_down(self.button2_press)
        self.button2.set_text("Rotate")
        
        self.slider = BL_UI_Slider(20, 20, 260, 30)
        self.slider.set_color((0.2, 0.8, 0.8, 0.8))
        self.slider.set_hover_color((0.2, 0.9, 0.9, 1.0))
        self.slider.set_min(0.0)
        self.slider.set_max(5.0)
        self.slider.set_value(2.0)
        self.slider.set_decimals(1)
        self.slider.set_value_change(self.on_slider_value_change)

        self.widgets = [self.panel, self.button1, self.button2, self.slider]
        
        self.panel.add_widgets([self.button1, self.button2, self.slider])
        
    def on_slider_value_change(self, slider, value):
        active_obj = bpy.context.view_layer.objects.active
        if active_obj is not None:
            active_obj.scale = (1, 1, value)

    # Button press handlers    
    def button1_press(self, widget):
        self.slider.set_value(3.0)
        print("Button '{0}' is pressed".format(widget.text))

        
    def button2_press(self, widget):
        print("Button '{0}' is pressed".format(widget.text))
        active_obj = bpy.context.view_layer.objects.active
        if active_obj is not None:
            active_obj.rotation_euler = (0, 30, 90)