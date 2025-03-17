"""
postprocessor_interface.py

Defines:
  - Sections: constants to identify sections in G-code (e.g. Cura markers)
  - PrintProcessorInterface: abstract interface for post-processing G-code
  - CollectionProcessorInterface: abstract interface for collecting data
"""

from abc import ABC, abstractmethod

class Sections:
    """
    Collection of constants/markers for G-code segmentation.
    """
    TOP_COMMENT_SECTION       = "TOP_COMMENT"
    STOP_COMMENT_SECTION      = "STOP_COMMENT"
    STARTUP_SCRIPT_SECTION    = "STARTUP_SCRIPT"
    GCODE_MOVEMENTS_SECTION   = "GCODE_MOVEMENTS"
    END_SCRIPT_SECTION        = "END_SCRIPT"
    BOTTOM_COMMENT            = "BOTTOM_COMMENT"

    # Common slicer markers (e.g., Cura)
    CURA_LAYER                = ";LAYER:"
    CURA_MESH_LAYER           = ";MESH"
    CURA_OUTER_WALL           = ";TYPE:WALL-OUTER"
    CURA_TYPE_LAYER           = ";TYPE"

    END_OF_HEADER_SETTINGS_MARLIN  = ";MAXZ:"
    END_OF_HEADER_SETTINGS_GRIFFIN = ";END_OF_HEADER"
    END_OF_TOP_METADATA            = ";Generated with Cura"
    END_OF_STARTUP_SCRIPT          = ";LAYER_COUNT:"
    END_OF_GCODE_MOVEMENTS         = ";TIME_ELAPSED"
    END_OF_GCODE                   = ";End of Gcode"

class PrintProcessorInterface(ABC):
    """
    Abstract interface for a "post-processor" that modifies or augments
    an entire stream of G-code.
    """

    @abstractmethod
    def process(self, gcode: str) -> str:
        """
        Takes a G-code string, transforms it, and returns the modified G-code.
        """
        raise NotImplementedError

class CollectionProcessorInterface(ABC):
    """
    Abstract interface for collecting or generating additional data
    that might be used for dynamic post-processing.
    """

    @abstractmethod
    def collect(self):
        """
        Gathers or computes data required for dynamic post-processing.
        """
        raise NotImplementedError
