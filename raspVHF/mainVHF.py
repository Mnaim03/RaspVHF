from rtlsdr import RtlSdr
import numpy as np
import time
from collections import deque
import signal

from Handler.vhfHandler import *
from Handler.checkHandler import *
from Handler.arduinoHandler import *

# Configurazione SDR
sdr = RtlSdr()

# Parametri
THRESHOLD_MARGIN_DB = Parameters.THRESHOLD_MARGIN_DB
MIN_BANDWIDTH_HZ = Parameters.MIN_BANDWIDTH_HZ
MAX_BANDWIDTH_HZ = Parameters.MAX_BANDWIDTH_HZ
MIN_PEAK_CONFIRMATIONS = Parameters.MIN_PEAK_CONFIRMATIONS
COOLDOWN_PERIOD = Parameters.COOLDOWN_PERIOD
# Per stimare rumore in modo stabile, uso una finestra temporale di medie
NOISE_ESTIMATION_WINDOW = Parameters.NOISE_ESTIMATION_WINDOW

# Code per memorizzare le medie di rumore degli ultimi blocchi
noise_floor_history = deque(maxlen=NOISE_ESTIMATION_WINDOW)

# Variabili stato
detection_count = 0
last_detection_time = 0

#Arduino
Arduino = start_Arduino()

#Ogetto di cHck
check = lastInput()


def rileva_segnale(samples):
    global detection_count, last_detection_time

    # Applico finestra Hann per ridurre leakage
    windowed = samples * np.hanning(len(samples))

    # FFT e spettro in potenza (dB)
    spectrum = np.fft.fftshift(np.fft.fft(windowed))
    power = 10 * np.log10(np.abs(spectrum)**2 + 1e-12)

    # Frequenze associate
    freqs = np.linspace(-sdr.sample_rate/2, sdr.sample_rate/2, len(power)) + sdr.center_freq

    # Stima rumore attuale: uso la mediana (meno influenzata dai picchi)
    noise_estimate = np.median(power)
    noise_floor_history.append(noise_estimate)

    # Rumore medio storico (da ultimi blocchi)
    noise_floor_avg = np.mean(noise_floor_history)

    # Soglia adattiva (media + margine)
    threshold = noise_floor_avg + THRESHOLD_MARGIN_DB

    max_power = np.max(power)
    mean_power = np.mean(power)

    if max_power > threshold:
        indices = np.where(power > threshold)[0]
        if len(indices) > 1:
            bandwidth = freqs[indices[-1]] - freqs[indices[0]]
        else:
            bandwidth = 0

        if (MIN_BANDWIDTH_HZ * unit_to_multiplier(get_frequence_hz())) < bandwidth < (MAX_BANDWIDTH_HZ * unit_to_multiplier(get_frequence_hz())):
            detection_count += 1
            peak_freq = freqs[np.argmax(power)]

            # Conferma più rilevazioni consecutive e rispetto cooldown
            if (detection_count >= MIN_PEAK_CONFIRMATIONS) and (time.time() - last_detection_time) > COOLDOWN_PERIOD:

                last_detection_time = time.time()

                clear_terminal()
                print(f"[⚠️ ATTIVITÀ RILEVATA] Frequenza: {peak_freq/1e6:.4f} MHz | "
                      f"BW: {bandwidth/1e3:.1f} kHz | Potenza: {max_power:.1f} dB | "
                      f"Soglia: {threshold:.1f} dB | Rumore medio: {noise_floor_avg:.1f} dB")
                #tampa_ascii_spectrum(freqs, power, threshold)

                detection_count = 0
                set_anomalia(True)

                return True

    else:

        # Output per debug (aggiorna in linea)
        clear_terminal()
        print(f"[✓ Normale] Max: {max_power:.1f} dB | Soglia: {threshold:.1f} dB | Rumore: {noise_floor_avg:.1f} dB | Freq: {get_frequence_num()} {get_frequence_hz()} ", end='\r')
        # stampa_ascii_spectrum(freqs, power, threshold)

        detection_count = 0
        set_anomalia(False)

    return False


def main():
    global flag_change

    #compile_Arduino()
    update_arduino(Arduino)

    try:
        while True:
            #Stampa Arduino in caso necessario
            if check.checkChange():
                update_arduino(Arduino)

            #VHF/Raspberry
            set_freuqneza_sdr(sdr)

            for _ in range(5):
                sdr.read_samples(1024)

            signal.alarm(1)  # 1 secondi timeout
            samples = sdr.read_samples(1024 * 64)


            rileva_segnale(samples)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nInterruzione manuale")
        end_Arduino(Arduino)

    finally:
        sdr.close()
        Arduino.close()
        print("Dispositivo SDR e Arduino rilasciato")




if __name__ == "__main__":
    main()
