import serial
import time
from mainHandler import update_raspberry, arduino_end

serial_port = "/dev/ttyACM0"

#invio valori al mio arduino...

# Configura la connessione seriale
arduino = serial.Serial(serial_port, 9600)
time.sleep(2)  # Attendi che la connessione si stabilisca

# Invia valori 1 e 2 in modo ciclico con attesa
try:
    while True: #ciclo infinito
        for flag in [1, 2]:

            update_raspberry(arduino)

            print(f"Inviato: {flag}")

            time.sleep(5)
except KeyboardInterrupt: #chiusura da tastiera

    print("Interrotto dall'utente")

    arduino_end()
finally:
    arduino.close()