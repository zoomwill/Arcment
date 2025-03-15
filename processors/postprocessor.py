from PostProcessors import *
from collections import defaultdict

class PostProcessor():
  
  def __init__(self):
    """Initializes the PostProcessors class
    gcode: list[list[str]]: List of List of strings where each list is a layer of gcode"""
    
    self.layer_index = 0 # Current layer index
    
  def collect_laser(self):
    """Collects the laser path gcode for the next layer"""
    current_layer = self.gcode[self.layer_index]
    
  def gen_next_layer():
    """Generates the next layer of gcode"""
    pass
  

    