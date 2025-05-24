import serial
import time
from handler import set_frequenza_num, set_frequenza_hz, set_anomalia, get_frequence_num, get_frequence_hz

serial_port = "/dev/ttyACM0"

#invio valori al mio arduino...

# Configura la connessione seriale
arduino = serial.Serial(serial_port, 9600)
time.sleep(2)  # Attendi che la connessione si stabilisca

# Invia valori 1 e 2 in modo ciclico con attesa
try:
    while True: #ciclo infinito
        for flag in [1, 2]:

            # 1 -> No Anomalia
            # 2 -> Anomalia
            arduino.write(f"{flag}\n".encode())
            #stampa seriale
            arduino.write(f"{get_frequence_num()}\n".encode())
            arduino.write(f"{get_frequence_hz()}\n".encode())

            #Stampo sul sito web i dati necessari
            #attulmente stampa ciò che ha ottenito sul sito stesso :-)
            set_frequenza_num({get_frequence_num()})
            set_frequenza_hz({get_frequence_hz()})
            if flag == 1:
                set_anomalia(False)
            else:
                set_anomalia(True)

            print(f"Inviato: {flag}")

            time.sleep(5)
except KeyboardInterrupt: #chiusura da tastiera

    print("Interrotto dall'utente")
    # stampa seriale
    # 3 -> Fine Ricezione
    arduino.write(f"{3}\n".encode()) #printo fine esecuzione
finally:
    arduino.close()