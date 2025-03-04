from .postprocessor_interface import Sections, PrintProcessorInterface, CollectionProcessorInterface
from collections import defaultdict

class PostProcessors():
  
  def __init__(self, gcode: list[list[str]]):
    """Initializes the PostProcessors class
    gcode: list[list[str]]: List of List of strings where each list is a layer of gcode"""
    
    self.gcode = gcode 
    self.print_processors = [] # Processors for movement related to printing: Uses PrintProcessorInterface
    self.collection_processors = [] # Processors for movement related to data collection: CollectionProcessorInterface
    self.layer_index = 0 # Current layer index
    
  def collect(self):
    """Calls sensors and get data from them"""
    
    for processor in self.collection_processors:
      
      if not isinstance(processor, CollectionProcessorInterface):
        raise TypeError(f"{processor} does not implement CollectionProcessorInterface")
      
      processor.collect()
  
  def process_layer(self):
    """Processes the current layer"""
    
    current_layer = self.gcode[self.layer_index]
    
    for processor in self.movement_processors:
      current_layer = processor.process(current_layer)