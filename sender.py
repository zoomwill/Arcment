import requests
import RepRapFirmwareAPI
from processors.preprocessors.preprocessors import PreProcessor
from processors.preprocessors.layer_parser import LayerParser
from processors.preprocessors.processor_interface import Sections, ProcessorInterface


class Sender():
  
  def __init__(self, gcode):
    self.gcode = gcode
    self.duet_ip = "192.254.1.2"
    self.rrf = RepRapFirmwareAPI.RepRapFirmwareAPI(self.duet_ip)
    
    preprocessor = PreProcessor(gcode)
    layers = preprocessor.parse_layers()
    self.send_gcode_layer(layers[1])
    
  def send_gcode_layer(self, command):
    """Send gcode to printer"""
    for line in command: 
      self.rrf.gcode(line, "async")
      esp = self.rrf.reply()
      print(esp)
      
if __name__ == "__main__":
  Sender("test.gcode")