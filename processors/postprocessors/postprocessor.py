from .postprocessor_interface import Sections, PrintProcessorInterface, CollectionProcessorInterface
from collections import defaultdict

class PostProcessors():
  
  def __init__(self, gcode: list[list[str]]):
    """Initializes the PostProcessors class
    gcode: list[list[str]]: List of List of strings where each list is a layer of gcode"""
    
    self.gcode = gcode 
    self.layer_index = 0 # Current layer index
    
  def collect_laser(self):
    """Collects the laser path gcode for the next layer"""
    current_layer = self.gcode[self.layer_index]
    
    # Generate gcode for laser movement

    