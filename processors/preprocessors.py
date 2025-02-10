from typing import List
from processor_interface import ProcessorInterface, Sections

class PreProcessor():
  
  def __init__(self, gcode: List[str], processors: List[ProcessorInterface]):
    self.gcode = gcode
    self.section_processors = {Sections.TOP_COMMENT_SECTION : [],
                               Sections.STARTUP_SCRIPT_SECTION : [],
                               Sections.GCODE_MOVEMENTS_SECTION : [],
                               Sections.END_SCRIPT_SECTION : [],
                               Sections.BOTTOM_COMMENT : []}
    
  def run_processors(self, gcode: List[str] = None) -> List[str]:
    
    if gcode is None:
      gcode = self.gcode
      
    # Add processors to their respective sections
    for processor in self.section_processors: 
      processor_type = processor.process_type()
      self.section_processors[processor_type].append(processor)
    # Run processors in order
    # Order: TOP_COMMENT, STARTUP_SCRIPT, GCODE_MOVEMENTS, END_SCRIPT, BOTTOM_COMMENT
      
    return gcode
  
  def get_top_section(self):
    top_section = []
    
    