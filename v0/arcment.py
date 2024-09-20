import requests

duet_ip = "192.168.0.4"


def send_gcode(command):
    url = f"http://{duet_ip}/rr_gcode?gcode={command}"
    response = requests.get(url)
    return response.json()


def main():
    filename = input("Please enter a gcode file to run: ")
    with open(filename, "r") as file:
        gcode_commands = file.readlines()
    for command in gcode_commands:
        response = send_gcode(command)
        print(response)


if __name__ == "__main__":
    main()