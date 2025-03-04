from .postprocessor_interface import Sections, PrintProcessorInterface

class LaserPathGcode(PrintProcessorInterface):
  """This processor will generate the laser path gcode to scan over the print area for the next layer"""

  def __init__(self, gcode: list[str]) -> list[str]:
    self.gcode = gcode
    self.min_x = None
    self.max_x = None
    self.min_y = None
    self.max_y = None
    self.z = None
    
    self.extract_coordinates()
    
  def process(self):
    pass
  
  def extract_coordinates(self):
    """Gets borderline coordnates for next layer's print"""
    
    for line in self.gcode:
      if line.startswith('G1'):
        x = float(line.split('X')[1].split(' ')[0])
        y = float(line.split('Y')[1].split(' ')[0])
        z = float(line.split('Z')[1].split(' ')[0])
        
        if self.min_x == None:
          self.min_x = x
        elif x < self.min_x:
          self.min_x = x
          
        if self.max_x == None:
          self.max_x = x
        elif x > self.max_x:
          self.max_x = x
          
        if self.min_y == None:
          self.min_y = y
        elif y < self.min_y:
          self.min_y = y
          
        if self.max_y == None:
          self.max_y = y
        elif y > self.max_y:
          self.max_y = y
          
        self.z = z