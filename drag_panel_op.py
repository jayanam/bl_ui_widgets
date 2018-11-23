import bpy

from bpy.types import Operator
 
from . bl_ui_button import *
from . bl_ui_drag_panel import *
    
class DP_OT_draw_operator(Operator):
    bl_idname = "object.dp_ot_draw_operator"
    bl_label = "bl ui widgets operator"
    bl_description = "Operator for bl ui widgets" 
    bl_options = {'REGISTER'}
    	
    @classmethod
    def poll(cls, context):
        return True
    
    def __init__(self):
        self.draw_handle = None
        self.draw_event  = None
        
        self.button1 = BL_UI_Button(20, 20, 120, 30)
        self.button1.set_bg_color((1.0, 0.2, 0.2, 0.8))
        self.button1.set_mouse_down(self.button1_press)
        self.button1.set_text("Scale")
        
        self.button2 = BL_UI_Button(160, 20, 120, 30)
        self.button2.set_bg_color((0.0, 0.2, 1.0, 0.8))
        self.button2.set_mouse_down(self.button2_press)
        self.button2.set_text("Rotate")
        
        self.panel = BL_UI_Drag_Panel(300,300,300,100)
        self.panel.set_bg_color((0.5, 1.0, 1.0, 0.6))
    
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
        
    def invoke(self, context, event):
        args = (self, context)
                   
        self.register_handlers(args, context)
                   
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}
    
    def register_handlers(self, args, context):
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_px, args, "WINDOW", "POST_PIXEL")
        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)
        
    def unregister_handlers(self, context):
        
        context.window_manager.event_timer_remove(self.draw_event)
        
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, "WINDOW")
        
        self.draw_handle = None
        self.draw_event  = None
          
    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()
        
        # TODO: Refactor this  
        if self.button1.handle_event(event) or self.button2.handle_event(event) or self.panel.handle_event(event):
            return {'RUNNING_MODAL'}   
        
        if event.type in {"ESC"}:
            self.unregister_handlers(context)
            return {'CANCELLED'}
                    
        return {"PASS_THROUGH"}
                                
    def finish(self):
        self.unregister_handlers(context)
        return {"FINISHED"}
		
	# Draw handler to paint onto the screen
    def draw_callback_px(self, context, args):
        print(args)
        self.button1.draw()
        self.button2.draw()  
        self.panel.draw() 