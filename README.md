# Arcment
![Arcment](https://github.com/user-attachments/assets/c6863c79-2406-4356-9734-56b29bb721a2)

This software processes and prints G-code **line by line** while using a **laser path planning system** to dynamically adjust the **Z-axis**, ensuring uniform bead deposition. The system operates in several stages:  

## **1. G-code Parsing (`gcode_parser`)**  
- The software starts by **interpreting the generated G-code**, which contains instructions for the printing process.  

## **2. Preprocessing (`preprocessors`)**  
- Before the print starts, **preprocessors modify the G-code** to prepare necessary adjustments, such as:  
  - Laser path adjustments  
  - Initial Z-axis modifications  
  - Other preparatory modifications  

## **3. Sending G-code (`sender`)**  
- The `sender` transmits the **G-code layer by layer** to the printer, ensuring controlled execution.  

## **4. Postprocessing (`postprocessors`)**  
- During printing, **postprocessors dynamically modify the G-code in real time** by:  
  - Adjusting the laser scanning path
  - Computing and modifying the next layer’s G-code  
  - Other future features that are required to be processed during the print

## **5. Receiving Sensor Data (`receiver`)**  
- The `receiver` module **communicates with external sensors** to collect real-time data:  
  - Laser readings  
  - Temperature readings  

## **6. Duet Board (`Duet`)**  
- The **Duet control board** manages execution, processing received G-code and sensor data for adaptive printing.  

## **7. Sensors (`Sensors`)**  
- **Laser and temperature sensors** provide real-time data, which is used to:  
  - Dynamically adjust the Z-axis  
  - Ensure uniform bead formation  
