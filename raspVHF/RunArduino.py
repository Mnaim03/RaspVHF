import subprocess

sketch_path = "/home/user1/Documents/RaspVHF/raspVHF/arduino/arduino.ino"
fqbn = "arduino:avr:uno"
serial_port = "/dev/ttyACM0"

# Compilazione
try:
    subprocess.run(["arduino-cli", "compile", "--fqbn", fqbn, sketch_path], check=True)
    print("Compilazione riuscita")
except subprocess.CalledProcessError:
    print("Errore nella compilazione")

# Upload
try:
    subprocess.run(["arduino-cli", "upload", "-p", serial_port, "--fqbn", fqbn, sketch_path], check=True)
    print("Upload riuscito")
except subprocess.CalledProcessError:
    print("Errore nell'upload")
