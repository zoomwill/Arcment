"""
postprocessor_main.py

This script is the main entry point for post-processing. It:
  1. Reads in an existing G-code file (the "next layer" or entire job).
  2. Uses LaserPathGcode to build & insert laser scanning moves for the new layer.
  3. Uses LaserDataCollector to acquire & process sensor measurements (through OxApi or other).
  4. Calculates an appropriate Z-offset based on measured height error.
  5. Outputs or sends the updated G-code lines to the printer (e.g., via Duet HTTP).

Usage:
    python postprocessor_main.py input_file.gcode output_file.gcode
"""

import sys
from typing import List

# Example: If your code is in a package, fix the imports accordingly:
from laser_path_gcode import LaserPathGcode
from data_collector import LaserDataCollector
from postprocessor import PostProcessors
from postprocessor_interface import PrintProcessorInterface


def main():
    if len(sys.argv) < 3:
        print("Usage: python postprocessor_main.py <input_gcode> <output_gcode>")
        sys.exit(1)

    input_gcode_file = sys.argv[1]
    output_gcode_file = sys.argv[2]

    # Read the entire G-code
    with open(input_gcode_file, "r") as f:
        gcode_lines = f.read().splitlines()

    # 1) Build laser scanning path for the new layer (or for each layer).
    #    This example just does one pass. Modify to detect multiple layers if needed.
    scanner = LaserPathGcode(gcode_lines)
    scan_moves = scanner.build_scan_moves()  # returns a list of lines that move the sensor

    # Insert these scan moves near the top or after you finish the last layer, etc.
    # For demonstration, we'll just prepend them (real placement is up to you).
    combined_gcode = scan_moves + gcode_lines

    # 2) Collect sensor data using the LaserDataCollector (which calls OxApi / pythonnet).
    collector = LaserDataCollector()
    measured_height_error = collector.collect_data()  # returns e.g. a float or an average offset

    # 3) Post-process the entire G-code with the sensor-based offset. 
    #    For example, we apply a single offset to the next layer’s Z. 
    #    If you have multiple layers, you might do it per-layer.
    # 
    # Example: we feed the combined G-code into a PostProcessors that 
    # interprets the final offset from the sensor measurements.
    processor = PostProcessors(sensor_based_offset=measured_height_error)
    final_gcode_str = processor.process("\n".join(combined_gcode))

    # 4) Write final G-code to an output file
    with open(output_gcode_file, "w") as out_f:
        out_f.write(final_gcode_str)

    print(f"[INFO] Finished post-processing. Output -> {output_gcode_file}")


if __name__ == "__main__":
    main()
