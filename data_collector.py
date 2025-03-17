"""
data_collector.py

Demonstrates how to interface with the OxApi-based sensor
to retrieve measurement data. The 'collect_data()' method
should return a numeric offset for the next-layer Z,
based on the real measured top of the printed part.
"""

import math
# from your_oxapi_module import ox  # e.g. from .oxapi import ox
# Or whatever you named the class that wraps the .NET assembly

class LaserDataCollector:
    """
    Collects data from the laser sensor (via the OxApi pythonnet interface),
    interprets / cleans it, and returns a recommended Z-offset.
    """

    def __init__(self, ip_address="192.168.0.10", streaming_port=1234):
        self.ip_address = ip_address
        self.port = streaming_port
        self.sensor_client = None  # an instance of `ox` from your code

    def setup_sensor(self):
        """
        Example of connecting to sensor with your .NET wrapper.
        The code below is indicative. Adjust for your local environment.
        """
        # self.sensor_client = ox(self.ip_address, self.port)
        # self.sensor_client.Connect()
        # self.sensor_client.Login()
        # ...
        pass

    def collect_data(self) -> float:
        """
        Acquire measurement(s) from the sensor, do any needed
        processing or averaging, then decide how much offset
        we should apply to the next layer's Z.
        Returns:
            A float offset in mm. Positive means we raise the Z,
            negative means we lower it.
        """

        # Example pseudo-code:
        # self.setup_sensor()
        #
        # # read e.g. 10 samples
        # sample_values = []
        # for i in range(10):
        #     block_id, config_mode, timestamp, synced, valid, quality, alarm, outputs, meas_rate, enc_val, values = \
        #         self.sensor_client.stream.ReadMeasurement()
        #     if valid:
        #         # Suppose 'values[0]' is a height reading (mm) from the sensor
        #         sample_values.append(values[0])
        #
        # # do a simple average
        # if len(sample_values) > 0:
        #     average_height = sum(sample_values)/len(sample_values)
        # else:
        #     average_height = 0.0
        #
        # # Suppose we want the next layer's top to be at e.g. +1.0 mm from average
        # # In reality you will compare average_height to the "expected" and compute error
        # expected_top = 10.0  # hypothetical
        # measured_error = (expected_top - average_height)
        #
        # offset_for_next_layer = measured_error
        # # close connections if needed
        #
        # return offset_for_next_layer

        # For now, let's just return a stub offset
        return 0.15  # mm - e.g. we discovered it's 0.15 mm too low

