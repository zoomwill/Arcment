 The goal:

Post‑processor main file: Orchestrates reading the original G‑code, scanning with the laser, collecting data, and rewriting the G‑code for the next layer.
Modules for:
Generating laser path G‑code to scan the printed area
Mapping laser‐sensor data to coordinates
Interpreting/cleaning the data
Generating the next‐line G‑code offsets
Only Z-height is being adjusted.

How these're gonna work: 
postprocessor_main.py loads the original G‑code, constructs a laser scan path (via LaserPathGcode), collects sensor data (via LaserDataCollector), then passes everything to PostProcessors to insert the final offset into the Z commands.
laser_path_gcode.py extracts bounding box info (min/max X/Y) and returns scanning G‑code lines so you can measure your print’s top.
data_collector.py demonstrates hooking into the Baumer/OxApi sensor (via pythonnet). In real code, you’d implement the reading/averaging logic, returning a final numeric offset.
postprocessor.py modifies the G‑code with the offset. In this example, it either inserts G0 Z+xxx lines or modifies the existing Z lines, according to your preference.
postprocessor_interface.py is the base interface.
