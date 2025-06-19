import os
from datetime import datetime

percorso="/var/www/html/Data"
logs="/var/www/html/logs.txt"

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def modifica_valore(chiave, nuovo_valore):
    righe_modificate = []
    trovato = False

    with open(percorso, "r") as f:
        righe = f.readlines()

    for riga in righe:
        if riga.strip().startswith(chiave + " ="):
            righe_modificate.append(f"{chiave} = {nuovo_valore}\n")
            trovato = True
        else:
            righe_modificate.append(riga)

    if not trovato:
        righe_modificate.append(f"{chiave} = {nuovo_valore}\n")

    with open(percorso, "w") as f:
        f.writelines(righe_modificate)

def set_frequenza_num(nuovo_numero):
    modifica_valore("frequence_num", nuovo_numero)

def set_frequenza_hz(unita):
    modifica_valore("frequence_hz", unita)

def set_anomalia(stato):  # 'true' o 'false'
    stato_str = "true" if stato else "false"
    modifica_valore("anomalia", stato_str)

def update_logs():
    try:
        with open(logs, "r") as f:
            contenuto = f.read()
    except FileNotFoundError:
        contenuto = ""

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    riga = f"{timestamp}: Anomalia su {get_frequence_num()} {get_frequence_hz()}"

    with open(logs, "w") as f:
        f.write(riga.strip() + "\n" + contenuto)

def get_frequence_num():
    try:
        with open(percorso, "r") as f:
            for riga in f:
                if riga.startswith("frequence_num"):
                    return int(riga.strip().split("=")[1].strip())
    except Exception as e:
        print(f"Errore nella lettura di frequence_num: {e}")
    return None

def get_frequence_hz():
    try:
        with open(percorso, "r") as f:
            for riga in f:
                if riga.startswith("frequence_hz"):
                    return riga.strip().split("=")[1].strip()
    except Exception as e:
        print(f"Errore nella lettura di frequence_hz: {e}")
    return None

def get_anomalia():
    try:
        with open(percorso, "r") as f:
            for riga in f:
                if riga.startswith("anomalia"):
                    return riga.strip().split("=")[1].strip()
    except Exception as e:
        print(f"Errore nella lettura di get_anomala: {e}")
    return None
