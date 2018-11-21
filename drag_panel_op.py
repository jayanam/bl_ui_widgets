import bpy

from bpy.types import Operator
 
from . drag_panel import *
    
class DP_OT_draw_operator(Operator):
    bl_idname = "object.dp_ot_draw_operator"
    bl_label = "Drag Panel"
    bl_description = "Drag Panel example" 
    bl_options = {'REGISTER'}
    	
    @classmethod
    def poll(cls, context):
        return True
    
    def __init__(self):
        self.draw_handle = None
        self.draw_event  = None
        self.panel = Drag_Panel(20, 20, 300, 100)
        self.panel.set_color((1.0, 0.2, 0.2, 1.0))

    def invoke(self, context, event):
        args = (self, context)
        
        if(context.window_manager.DP_started is False):
            context.window_manager.DP_started = True
                
            # Register draw callback
            self.register_handlers(args, context)
                       
            context.window_manager.modal_handler_add(self)
            return {"RUNNING_MODAL"}
        else:
            context.window_manager.DP_started = False
            return {'CANCELLED'}
    
    def register_handlers(self, args, context):
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_px, (self, context), "WINDOW", "POST_PIXEL")
        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)
        
    def unregister_handlers(self, context):
        
        context.window_manager.event_timer_remove(self.draw_event)
        
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, "WINDOW")
        
        self.draw_handle = None
        self.draw_event  = None
     
           
    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()
                
        if context.area.type == 'VIEW_3D':
            if self.panel.handle_event(event):
                return {'RUNNING_MODAL'}   
        
        if event.type in {"ESC"}:
            context.window_manager.DP_started = False
        
        if not context.window_manager.DP_started:
            self.unregister_handlers(context)
            return {'CANCELLED'}
               
        return {"PASS_THROUGH"}
                            
        
    def cancel(self, context):
        if context.window_manager.DP_started:
            self.unregister_handlers(context)
        return {'CANCELLED'}        
        
    def finish(self):
        self.unregister_handlers(context)
        return {"FINISHED"}
		
	    # Draw handler to paint onto the screen
    def draw_callback_px(self, context, args):
        self.panel.draw()
        
        