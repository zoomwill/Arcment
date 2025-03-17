"""
laser_path_gcode.py

Defines a class to generate G-code that drives the laser scanner
over the region that was just printed, so we can measure height.
"""

from postprocessor_interface import PrintProcessorInterface


class LaserPathGcode(PrintProcessorInterface):
    """
    Generates extra scanning moves to measure the top surface
    of the just-printed region. We assume we only measure once
    here, but you could adapt it to measure multiple times or
    along multiple scan lines.
    """

    def __init__(self, gcode_lines):
        """
        :param gcode_lines: list of G-code lines. We'll attempt
                            to parse bounding X/Y min and max.
        """
        self.gcode_lines = gcode_lines
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None
        self.last_z = 0.0
        self.extract_coordinates()

    def extract_coordinates(self):
        """
        Looks through the existing G-code lines, tries to find min/max
        X/Y, and the last Z used. This is a simplistic approach.
        """
        for line in self.gcode_lines:
            if line.startswith("G1") and ("X" in line) and ("Y" in line):
                # Example parse for X, Y, Z
                tokens = line.split()
                x_val, y_val, z_val = None, None, None
                for t in tokens:
                    if t.startswith("X"):
                        x_val = float(t[1:])
                    elif t.startswith("Y"):
                        y_val = float(t[1:])
                    elif t.startswith("Z"):
                        z_val = float(t[1:])
                # Update min/max
                if x_val is not None:
                    if self.min_x is None or x_val < self.min_x:
                        self.min_x = x_val
                    if self.max_x is None or x_val > self.max_x:
                        self.max_x = x_val
                if y_val is not None:
                    if self.min_y is None or y_val < self.min_y:
                        self.min_y = y_val
                    if self.max_y is None or y_val > self.max_y:
                        self.max_y = y_val
                # Keep track of last Z if present
                if z_val is not None:
                    self.last_z = z_val

        if self.min_x is None:
            self.min_x = 0
        if self.max_x is None:
            self.max_x = 50
        if self.min_y is None:
            self.min_y = 0
        if self.max_y is None:
            self.max_y = 50

    def build_scan_moves(self):
        """
        Returns a list of G-code lines that move the sensor across
        the bounding region. You can refine speeds, feed rates, etc.
        """
        lines = []
        lines.append(";--- Begin Laser Scan Moves ---")
        # Move up a bit above the last printed Z:
        safe_z = self.last_z + 5.0
        lines.append(f"G0 Z{safe_z:.3f} F1200 ; move up to safe Z")
        # Move to min_x, min_y
        lines.append(f"G0 X{self.min_x:.3f} Y{self.min_y:.3f} F2000 ; start of scan")

        # Example: scanning in X direction from min_x to max_x
        lines.append(f"G1 Z{self.last_z + 1.0:.3f} F1200 ; get closer to top")
        lines.append("; (Activate Laser Sensor if needed)")

        # A single pass from min_x to max_x
        lines.append(f"G1 X{self.max_x:.3f} Y{self.min_y:.3f} F800 ; scanning pass")

        # Return to safe Z
        lines.append(f"G0 Z{safe_z:.3f} ; done scanning")
        lines.append(";--- End Laser Scan Moves ---")
        return lines

    def process(self, gcode: str) -> str:
        """
        This class also implements PrintProcessorInterface, but
        for demonstration, we return the input G-code unmodified.
        The real usage is to call build_scan_moves() in your
        main script and insert them as you choose.
        """
        return gcode  # No changes here
