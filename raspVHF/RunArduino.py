import subprocess
import serial
import time

sketch_path = "/home/user1/Documents/RaspVHF/raspVHF/arduino/arduino.ino"
fqbn = "arduino:avr:uno"
serial_port = "/dev/ttyACM0"

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


#invio valori al mio arduino...

# Configura la connessione seriale
arduino = serial.Serial(serial_port, 9600)
time.sleep(2)  # Attendi che la connessione si stabilisca

# Invia valori 0 e 1 in modo ciclico con attesa
try:
    while True: #ciclo infinito
        for flag in [0, 1]:
            arduino.write(f"{flag}\n".encode())
            print(f"Inviato: {flag}")
            time.sleep(1)
except KeyboardInterrupt: #chiusura da tastiera
    print("Interrotto dall'utente")
finally:
    arduino.close()
