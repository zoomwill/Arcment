import time
from processors import * 
from sender import *
from collection import *

class Main():
  
  def __init__(self, gcode_file):
    self.gcode_file = "test.gcode"
    self.preprocessor = PreProcessor(gcode_file)
    self.postprocessor = PostProcessor()
    self.sender = Sender()
    
    # Layer Logic
    self.layers = self.preprocessor.parse_layers()
    self.current_layer = 0
    self.total_layers = len(self.layers)
    
  def run(self):
    """
    Runs a single layer of the print with all processing
    Returns:
      bool: True if all layers are done, False otherwise
    """ 
    
    if self.current_layer >= self.total_layers:
      Exception("Layer index exceeds total layers")
    
    # Prints current layer 
    self.sender.send_layer(self.layers[self.current_layer])
    self.current_layer += 1
    print(f"Layer {self.current_layer} sent.")
    
    if self.current_layer == self.total_layers:
      # If all layers are done, exit
      print("All layers sent.")
      return True
    else:
      # Otherwise, generate next layer and replace current layer in queue 
      self.layers[self.current_layer] = self.postprocessor.gen_next_layer()
      return False
      
  def run_all(self):
    """Prints all layers"""
    while True:
      if self.run():
        break
      time.sleep(0.5)