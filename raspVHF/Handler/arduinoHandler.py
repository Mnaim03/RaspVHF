import time
import serial
import subprocess

from .dataHandler import *

"""
Modulo per la gestione della comunicazione tra Raspberry Pi e Arduino via porta seriale.

Include funzioni per:
- Avviare la connessione seriale con Arduino.
- Aggiornare lo stato e la frequenza sulla porta seriale.
- Segnalare la fine della trasmissione.
- Compilare e caricare lo sketch Arduino tramite arduino-cli.
"""

sketch_path = "/home/user1/Documents/RaspVHF/raspVHF/arduino/arduino.ino"
fqbn = "arduino:avr:uno"
serial_port = "/dev/ttyACM0"

"""
Inizializza la connessione seriale con Arduino.

Restituisce:
- Oggetto seriale attivo per comunicazione con Arduino.
"""
def start_Arduino():
    # Configura la connessione seriale
    Arduino = serial.Serial(serial_port, 9600)
    time.sleep(2)  # Attendi che la connessione si stabilisca
    return Arduino

"""
Invia lo stato di anomalia e i dati di frequenza all'Arduino via seriale.

Parametri:
- arduino: oggetto seriale attivo su cui scrivere.

Lo stato è codificato come:
- 1: nessuna anomalia
- 2: anomalia rilevata
"""
def update_arduino(arduino):
    # 1 -> No Anomalia
    # 2 -> Anomalia
    if get_anomalia() == "false" :
        flag = 1
    else:
        flag = 2

    arduino.write(f"{flag}\n".encode())
    # stampa seriale
    arduino.write(f"{get_frequence_num()}\n".encode())
    arduino.write(f"{get_frequence_hz()}\n".encode())
    arduino.flush()

"""
Invia ad Arduino il comando di fine esecuzione.

Parametri:
- arduino: oggetto seriale attivo su cui scrivere.

Codifica il valore "3" come segnale di terminazione.
"""
def end_Arduino(arduino):
    time.sleep(3)
    # attesa perchè potrebbe verificarsi che mentre mando input=3 sulla porta seriale non ci stia ancora alto

    # stampa seriale di 3 -> Fine Ricezione
    arduino.write(f"{3}\n".encode())  # printo fine esecuzione

"""
Compila e carica lo sketch Arduino utilizzando arduino-cli.

Esegue:
- Compilazione del file .ino.
- Upload sulla board Arduino tramite la porta seriale.

Stampa lo stato di avanzamento o eventuali errori.
"""
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


