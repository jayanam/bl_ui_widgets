from . bl_ui_widget import *

import blf
import bpy
from bpy.types import Operator
import sys
import os

class BL_UI_Background(BL_UI_Widget):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self._text_color        = (1.0, 1.0, 1.0, 1.0)
        self._hover_bg_color    = (0.5, 0.5, 0.5, 1.0)
        self._select_bg_color   = (0.7, 0.7, 0.7, 1.0)
        
        self._text = "Test"
        self._text_size = 16
        self._textpos = (x, y)

        self.__state = 0
        self.__image = None
        self.__image_size = (24, 24)
        self.__image_position = (4, 2)
    @property
    def hover_bg_color(self):
        return self._hover_bg_color

    @hover_bg_color.setter
    def hover_bg_color(self, value):
        self._hover_bg_color = value

    @property
    def select_bg_color(self):
        return self._select_bg_color

    @select_bg_color.setter
    def select_bg_color(self, value):
        self._select_bg_color = value 
        
    def set_image_size(self, imgage_size):
        self.__image_size = imgage_size

    def set_image_position(self, image_position):
        self.__image_position = image_position

    def set_image(self, rel_filepath):
        try:
            self.__image = bpy.data.images.load(rel_filepath, check_existing=True)   
            self.__image.gl_load()
            print (self.__image)
        except:
            pass

    def update(self, x, y):        
        super().update(x, y)
        self._textpos = [x, y]
        
    def draw(self):
        if not self.visible:
            return
            
        area_height = self.get_area_height()

        self.shader.bind()
        
        self.set_colors()
        
        bgl.glEnable(bgl.GL_BLEND)

        self.batch_panel.draw(self.shader) 

        self.draw_image()   

        bgl.glDisable(bgl.GL_BLEND)

        # Draw text
        #self.draw_text(area_height)

    def set_colors(self):
        color = self._bg_color
        text_color = self._text_color

        # pressed
        if self.__state == 1:
            color = self._select_bg_color

        # hover
        elif self.__state == 2:
            color = self._hover_bg_color

        self.shader.uniform_float("color", color)

    def draw_image(self):
        if self.__image is not None:
            try:
                y_screen_flip = self.get_area_height() - self.y_screen
        
                off_x, off_y =  self.__image_position
                sx, sy = self.__image_size
                
                # bottom left, top left, top right, bottom right
                vertices = (
                            (self.x_screen + off_x, y_screen_flip - off_y), 
                            (self.x_screen + off_x, y_screen_flip - sy - off_y), 
                            (self.x_screen + off_x + sx, y_screen_flip - sy - off_y),
                            (self.x_screen + off_x + sx, y_screen_flip - off_y))
                
                self.shader_img = gpu.shader.from_builtin('2D_IMAGE')
                self.batch_img = batch_for_shader(self.shader_img, 'TRI_FAN', 
                { "pos" : vertices, 
                "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1)) 
                },)

                bgl.glActiveTexture(bgl.GL_TEXTURE0)
                bgl.glBindTexture(bgl.GL_TEXTURE_2D, self.__image.bindcode)

                self.shader_img.bind()
                self.shader_img.uniform_int("image", 0)
                self.batch_img.draw(self.shader_img) 
                return True
            except:
                pass

        return False
