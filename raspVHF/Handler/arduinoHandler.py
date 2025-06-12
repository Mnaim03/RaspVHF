import time
import serial

from .mainHandler import *


def start_Arduino():
    serial_port = "/dev/ttyACM0"
    # Configura la connessione seriale
    Arduino = serial.Serial(serial_port, 9600)
    time.sleep(2)  # Attendi che la connessione si stabilisca
    return Arduino

def update_arduino(arduino):
    # 1 -> No Anomalia
    # 2 -> Anomalia
    if get_anomalia() == 1 : flag = 2
    else: flag = 1

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