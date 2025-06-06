percorso_scrittura="/var/www/html/outputData"
percorso_lettura="/var/www/html/inputData"

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

def unit_to_multiplier(unit):
    unit = unit.lower()
    return {
        "hz": 1,
        "khz": 1_000,
        "mhz": 1_000_000,
        "ghz": 1_000_000_000
    }.get(unit, 1)  # default = 1 Hz