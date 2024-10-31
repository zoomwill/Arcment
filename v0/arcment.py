import requests
import sys

duet_ip = "192.168.0.4"
x_offset = 10
y_offset = 11
z_offset = 12


def send_gcode(command):
    url = f"http://{duet_ip}/rr_gcode?gcode={command}"
    response = requests.get(url)
    return response.json()


def scan(z, x0, y0, x1, y1):
    z_buffer = 30
    init_move = [
        f"G1 Z{z+z_offset+z_buffer}",
        f"G1 X{x0+x_offset} Y{y0+y_offset} Z{z+z_offset}",
    ]


def print(z, x0, y0, x1, y1):
    pass


def main():
    filename = input("Please enter a gcode file to run: ")
    with open(filename, "r") as file:
        gcode_commands = file.readlines()
    movement_start = 0
    movement_end = 0
    end_script = 0
    z0 = 0
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    # Finds the start, end, and init z value 
    for i, command in enumerate(gcode_commands):
        if "Z" in command:
            comment_index = sys.maxsize
            if ";" in command:
                comment_index = command.index(";")
            if comment_index > command.index("Z"):
                z = float(command.split("Z")[1].split(" ")[0])
        if command.startswith(";TYPE:WALL-OUTER"):
            x0, y0 = float(gcode_commands[i-1].split("X")[1].split(" ")[0]), float(gcode_commands[i-1].split("Y")[1].split(" ")[0])
            z0 = float(gcode_commands[i+1].split("Z")[1].split(" ")[0])
            movement_start = i
        if command.startswith("M42 P1 S0"):
            x1, y1 = float(gcode_commands[i-3].split("X")[1].split(" ")[0]), float(gcode_commands[i-3].split("Y")[1].split(" ")[0])
            movement_end = i
        if command.startswith(";gcode movements end"):
            end_script = i
            break
        # response = send_gcode(command)
        # print(response)
    
    scan(z0, x0, y0, x1, y1)

    for i in range(movement_start, movement_end+1):
        command = gcode_commands[i]
        if command.startswith("G1"):
            if "X" in command:
                x = float(command.split("X")[1].split(" ")[0])
            if "Y" in command:
                y = float(command.split("Y")[1].split(" ")[0])
            if "Z" in command:
                z = float(command.split("Z")[1].split(" ")[0])
            gcode_commands[i] = f"G1 X{x+x_offset} Y{y+y_offset} Z{z+z_offset}"
        response = send_gcode(gcode_commands[i])
        print(response)
    for i in range(end_script, len(gcode_commands)):
        response = send_gcode(gcode_commands[i])
        print(response)


if __name__ == "__main__":
    main()