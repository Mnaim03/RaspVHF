import serial
import time

serial_port = "/dev/ttyACM0"

#invio valori al mio arduino...

# Configura la connessione seriale
arduino = serial.Serial(serial_port, 9600)
time.sleep(2)  # Attendi che la connessione si stabilisca

# Invia valori 0 e 1 in modo ciclico con attesa
try:
    while True: #ciclo infinito
        for flag in [1, 2]:

            #stampa seriale
            arduino.write(f"{flag}\n".encode())
            print(f"Inviato: {flag}")

            time.sleep(5)
except KeyboardInterrupt: #chiusura da tastiera

    print("Interrotto dall'utente")
    arduino.write(f"{3}\n".encode()) #printo fine esecuzione

finally:
    arduino.close()