import os
import time
import serial

percorso_scrittura="/var/www/html/outputData"
percorso_lettura="/var/www/html/inputData"

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def modifica_valore(chiave, nuovo_valore):
    righe_modificate = []
    trovato = False

    with open(percorso_scrittura, "r") as f:
        righe = f.readlines()

    for riga in righe:
        if riga.strip().startswith(chiave + " ="):
            righe_modificate.append(f"{chiave} = {nuovo_valore}\n")
            trovato = True
        else:
            righe_modificate.append(riga)

    if not trovato:
        righe_modificate.append(f"{chiave} = {nuovo_valore}\n")

    with open(percorso_scrittura, "w") as f:
        f.writelines(righe_modificate)


# GESTIONE FILE CONDIVISI

def set_frequenza_num(nuovo_numero):
    modifica_valore("frequence_num", nuovo_numero)

def set_frequenza_hz(unita):
    modifica_valore("frequence_hz", unita)

def set_anomalia(stato):  # 'true' o 'false'
    stato_str = "true" if stato else "false"
    modifica_valore("anomalia", stato_str)

def get_frequence_num():
    try:
        with open(percorso_lettura, "r") as f:
            for riga in f:
                if riga.startswith("frequence_num"):
                    return int(riga.strip().split("=")[1].strip())
    except Exception as e:
        print(f"Errore nella lettura di frequence_num: {e}")
    return None

def get_frequence_hz():
    try:
        with open(percorso_lettura, "r") as f:
            for riga in f:
                if riga.startswith("freuqnece_hz"):
                    return riga.strip().split("=")[1].strip()
    except Exception as e:
        print(f"Errore nella lettura di frequence_hz: {e}")
    return None

def get_anomalia():
    try:
        with open(percorso_scrittura, "r") as f:
            for riga in f:
                if riga.startswith("anomalia"):
                    return riga.strip().split("=")[1].strip()
    except Exception as e:
        print(f"Errore nella lettura di get_anomala: {e}")
    return None


# GESTIONE ARDUINO

def start_Arduino():
    serial_port = "/dev/ttyACM0"
    # Configura la connessione seriale
    Arduino = serial.Serial(serial_port, 9600)
    time.sleep(2)  # Attendi che la connessione si stabilisca
    return Arduino

def update_arduino(arduino):
    # 1 -> No Anomalia
    # 2 -> Anomalia
    if get_anomalia() == True : flag = 2
    else: flag = 1

    arduino.write(f"{flag}\n".encode())
    # stampa seriale
    arduino.write(f"{get_frequence_num()}\n".encode())
    arduino.write(f"{get_frequence_hz()}\n".encode())

def end_Arduino(arduino):
    time.sleep(3)
    # attesa perchè potrebbe verificarsi che mentre mando
    # input=3 sulla porta seriale ci stia ancora alto

    # stampa seriale
    # 3 -> Fine Ricezione
    arduino.write(f"{3}\n".encode())  # printo fine esecuzione