import os
from datetime import datetime

percorso="/var/www/html/Data"
logs="/var/www/html/logs.txt"

"""
Pulisce il terminale in base al sistema operativo.
Utilizza il comando 'cls' su Windows e 'clear' su sistemi Unix-like.
"""
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

"""
Modifica o aggiunge una coppia chiave-valore all'interno del file di configurazione.

Parametri:
- chiave: stringa che rappresenta la chiave da cercare.
- nuovo_valore: valore da assegnare alla chiave.

Se la chiave non è presente, viene aggiunta in fondo al file.
"""
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

"""
Imposta il valore numerico della frequenza nel file di configurazione.

Parametri:
- nuovo_numero: intero che rappresenta la frequenza.
"""
def set_frequenza_num(nuovo_numero):
    modifica_valore("frequence_num", nuovo_numero)

"""
Imposta il valore in Hertz della frequenza nel file di configurazione.

Parametri:
- unita: stringa che rappresenta la frequenza in Hz (es. "156.800 MHz").
"""
def set_frequenza_hz(unita):
    modifica_valore("frequence_hz", unita)

"""
Imposta lo stato di anomalia nel file di configurazione.

Parametri:
- stato: booleano; True per 'true', False per 'false'.
"""
def set_anomalia(stato):  # 'true' o 'false'
    stato_str = "true" if stato else "false"
    modifica_valore("anomalia", stato_str)

"""
Aggiunge un nuovo evento di anomalia al file di log, con timestamp e frequenza attuale.

Se il file di log non esiste, viene creato.
"""
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

"""
Legge e restituisce il valore numerico della frequenza dal file di configurazione.

Restituisce:
- intero se la lettura ha successo, altrimenti None.
"""
def get_frequence_num():
    try:
        with open(percorso, "r") as f:
            for riga in f:
                if riga.startswith("frequence_num"):
                    return int(riga.strip().split("=")[1].strip())
    except Exception as e:
        print(f"Errore nella lettura di frequence_num: {e}")
    return None

"""
Legge e restituisce la frequenza in formato stringa dal file di configurazione.

Restituisce:
- stringa se la lettura ha successo, altrimenti None.
"""
def get_frequence_hz():
    try:
        with open(percorso, "r") as f:
            for riga in f:
                if riga.startswith("frequence_hz"):
                    return riga.strip().split("=")[1].strip()
    except Exception as e:
        print(f"Errore nella lettura di frequence_hz: {e}")
    return None

"""
Legge e restituisce lo stato di anomalia dal file di configurazione.

Restituisce:
- stringa ('true' o 'false') se la lettura ha successo, altrimenti None.
"""
def get_anomalia():
    try:
        with open(percorso, "r") as f:
            for riga in f:
                if riga.startswith("anomalia"):
                    return riga.strip().split("=")[1].strip()
    except Exception as e:
        print(f"Errore nella lettura di get_anomala: {e}")
    return None
