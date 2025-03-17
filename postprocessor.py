"""
postprocessor.py

Implements a PostProcessors class that modifies G-code layer by layer,
inserting a custom Z offset based on sensor measurement.

Usage:
    from postprocessor import PostProcessors

    # Suppose we already have a measured offset from the laser collector
    measured_offset = 0.2

    # We'll apply that offset to each new layer:
    gcode_in = open("some_input.gcode").read()
    processor = PostProcessors(sensor_based_offset=measured_offset)
    gcode_out = processor.process(gcode_in)

    with open("out_postprocessed.gcode", "w") as f:
        f.write(gcode_out)
"""

from postprocessor_interface import (
    Sections, PrintProcessorInterface, CollectionProcessorInterface
)

class PostProcessors(PrintProcessorInterface, CollectionProcessorInterface):
    """
    A post-processor that dynamically adjusts the Z for each layer,
    applying the same measured offset (or you can track each layer’s
    own offset if you wish).
    """

    def __init__(self, sensor_based_offset: float = 0.0):
        """
        :param sensor_based_offset: The offset (in mm) from the sensor measurement.
                                    Positive -> raise the nozzle
                                    Negative -> lower the nozzle
        """
        self.sensor_based_offset = sensor_based_offset
        self.current_layer_index = 0

    def collect(self):
        """
        In a more complex scenario, you might do real-time sensor queries here.
        For now, we assume sensor_based_offset is already known.
        """
        pass

    def process(self, gcode: str) -> str:
        """
        Reads G-code line by line, looks for layer changes (CURA_LAYER),
        and inserts a small Z shift command or modifies lines that contain Z.
        Here we simply insert a new G-code line (G0 Z + offset).
        """
        lines = gcode.splitlines()
        processed = []

        for line in lines:
            # Detect a layer change from Cura
            if line.startswith(Sections.CURA_LAYER):
                # Optionally parse which layer number we're at
                layer_str = line[len(Sections.CURA_LAYER):].strip()
                try:
                    self.current_layer_index = int(layer_str)
                except ValueError:
                    self.current_layer_index += 1

                # We can call collect() or do anything else
                self.collect()

                # Insert a comment about applying the offset
                processed.append(f";--- [POSTPROC] Layer {self.current_layer_index}, adding sensor offset {self.sensor_based_offset:.3f} mm ---")
                # Insert a new Z move with the offset
                processed.append(f"G0 Z+{self.sensor_based_offset:.3f} ; sensor-based offset")

            # Keep the original line
            processed.append(line)

        return "\n".join(processed)
