import time
import serial
import subprocess

from .dataHandler import *

sketch_path = "/home/user1/Documents/RaspVHF/raspVHF/arduino/arduino.ino"
fqbn = "arduino:avr:uno"
serial_port = "/dev/ttyACM0"

def start_Arduino():
    # Configura la connessione seriale
    Arduino = serial.Serial(serial_port, 9600)
    time.sleep(2)  # Attendi che la connessione si stabilisca
    return Arduino

def update_arduino(arduino):
    # 1 -> No Anomalia
    # 2 -> Anomalia
    if get_anomalia() == "false" :
        flag = 1
    else:
        flag = 2

    print(f"{get_anomalia()} | {flag}")

    arduino.write(f"{flag}\n".encode())
    # stampa seriale
    arduino.write(f"{get_frequence_num()}\n".encode())
    arduino.write(f"{get_frequence_hz()}\n".encode())
    arduino.flush()

def end_Arduino(arduino):
    time.sleep(3)
    # attesa perchè potrebbe verificarsi che mentre mando
    # input=3 sulla porta seriale ci stia ancora alto

    # stampa seriale
    # 3 -> Fine Ricezione
    arduino.write(f"{3}\n".encode())  # printo fine esecuzione

def compile_Arduino():
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


