import blf
import bpy
from bpy.types import Operator
import sys
import os

from . bl_ui_label import * 
from . bl_ui_button import *
from . bl_ui_checkbox import *
from . bl_ui_slider import *
from . bl_ui_up_down import *
from . bl_ui_drag_panel import *
from . bl_ui_draw_op import *
from . bl_ui_background import *
    

bl_info = {
    "name": "BL UI Widgets_TEST_NEO",
    "description": "UI Widgets to draw in the 3D view",
    "author": "Jayanam, Olkeyn",
    "version": (0, 6, 4, 2),
    "blender": (2, 80, 0),
    "location": "View3D",
    "category": "Object"}

# Blender imports

from bpy.props import *
from bpy_extras.object_utils import AddObjectHelper
my_fork_addon_keymaps = []
DEFAULT_WIDGET_AREA = None
class DP_OT_draw_operator_fork_test(BL_UI_OT_draw_operator):
	bl_idname = "object.draw_operator_fork_test"
	bl_label = "bl ui widgets custom operator"
	bl_description = "Demo operator for bl ui widgets" 
	bl_options = {'REGISTER'}
	def __init__(self):
		print ('self ',self)
		if bpy.context.screen != None:
			print ("test_init")
			super().__init__()
			start_sreen = bpy.context.screen
			areas = []
			start_area = None
			for ar in start_sreen.areas.items(): # Checking if our layout have such area for our widgets
				if ar[1].type == 'VIEW_3D':
					areas.append(ar[1])
					start_area = ar[1]
					DEFAULT_WIDGET_AREA = ar[1]
			self.backgroundtest = BL_UI_Background (0, 0, 1, 1) 
			#Position and size of the container. It means that you can find a point where you cannot to set the cursor or make selection by mouse
			script_file = os.path.realpath(__file__)
			directory = os.path.dirname(script_file)
			image_path = directory+"//bitmap.png"
			print ('image', self.backgroundtest.set_image(image_path)) #
			self.backgroundtest.set_image_size((start_area.width-1, start_area.height-1)) # adjust size of the picture with the size of working area
			self.backgroundtest.set_image_position((0,0))
			self.backgroundtest.bg_color = (0.2, 0.9, 0.2, 0.5)
			self.button0 = BL_UI_Button(100, start_area.height-55, 100, 30)
			self.button0.bg_color = (0.9, 0.2, 0.2, 0.5)
			self.button0.text = 'NEO'
			self.button0.set_mouse_down(self.button0_press)

			self.button1 = BL_UI_Button(300, start_area.height-55, 100, 30)
			self.button1.bg_color = (0.2, 0.9, 0.2, 0.5)
			self.button1.text = 'TRINITY'
			self.button1.set_mouse_down(self.button1_press)

			self.button2 = BL_UI_Button(500, start_area.height-55, 100, 30)
			self.button2.bg_color = (0.2, 0.2, 0.9, 0.5)
			self.button2.text = 'MORPHEUS'
			self.button2.set_mouse_down(self.button2_press)
		    
			self.label = BL_UI_Label(20, 10, 100, 15)
			self.label.text = "Size:"
			self.label2 = BL_UI_Label(10, 20, 50, 15)
			self.label2.text = "Size:"
		else:
			print ('We have checked that layout not load yet and do nothing to avoid errors.')
	def on_invoke(self, context, event):
		# Add new widgets here (TODO: perhaps a better, more automated solution?)
		widgets = [self.button0,self.button1,self.button2,self.backgroundtest]
		self.init_widgets(context, widgets)
	def button0_press(self, widget):
		print("Button '{0}' is pressed".format(widget.text))
		gg = bpy.ops.mesh.primitive_ico_sphere_add()
		bpy.ops.ed.undo_push()	
		# very complicated moment, without it you can find disapointment to do almos all undo
		return gg
	def button1_press(self, widget):
		print("Button '{0}' is pressed".format(widget.text))
		gg = bpy.ops.mesh.primitive_cube_add()
		bpy.ops.ed.undo_push()
		# very complicated moment, without it you can find disapointment to do almos all undo
		return gg
	def button2_press(self, widget):
		print("Button '{0}' is pressed".format(widget.text))
		gg = bpy.ops.mesh.primitive_monkey_add()
		bpy.ops.ed.undo_push() 	
		# very complicated moment, without it you can find disapointment to do almos all undo
		return gg
