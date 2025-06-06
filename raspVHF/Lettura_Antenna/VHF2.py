from rtlsdr import RtlSdr
import numpy as np
import time
from collections import deque
import sys
import os

# Aggiungi la directory superiore al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from handler import get_frequence_num, get_frequence_hz, unit_to_multiplier, clear_terminal


# Configurazione SDR
sdr = RtlSdr()
sdr.gain = 'auto'

# Parametri
THRESHOLD_MARGIN_DB = 10        # Margine sopra rumore stimato
MIN_BANDWIDTH_HZ = 5000
MAX_BANDWIDTH_HZ = 25000
MIN_PEAK_CONFIRMATIONS = 3      # Quante rilevazioni consecutive per confermare
COOLDOWN_PERIOD = 2             # Secondi tra allarmi

# Per stimare rumore in modo stabile, uso una finestra temporale di medie
NOISE_ESTIMATION_WINDOW = 20    # Numero di blocchi per stimare rumore

# Code per memorizzare le medie di rumore degli ultimi blocchi
noise_floor_history = deque(maxlen=NOISE_ESTIMATION_WINDOW)

# Variabili stato
detection_count = 0
last_detection_time = 0

import os

def set_freuqneza_sdr():
    sdr.sample_rate = 2.4e6

    # Ottieni input
    input_freq = get_frequence_num()
    input_unit = get_frequence_hz()

    # Calcolo finale
    input_hz = unit_to_multiplier(input_unit)
    sdr.center_freq = int(input_freq * input_hz)

def stampa_ascii_spectrum(freqs, power, threshold):
    """Stampa una rappresentazione ASCII dello spettro centrata sulla soglia."""
    # Riduci a 80 punti per il terminale
    step = len(power) // 80
    reduced_power = power[::step][:80]

    # 🔧 Centra il grafico sulla soglia (es: da soglia-15 a soglia+5)
    display_min = threshold - 15
    display_max = threshold + 5
    scale = 25  # più righe = grafico più dettagliato

    print("\nSpettro (ASCII):")
    for level in reversed(np.linspace(display_min, display_max, scale)):
        line = ""
        for val in reduced_power:
            if val >= level:
                line += "█"
            elif abs(val - threshold) < 0.5:
                line += "-"
            else:
                line += " "
        print(f"{level:6.1f} | {line}")
    print("       +" + "-"*80)
    print("       |" + " " * 35 + "Frequenza →")


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

        if MIN_BANDWIDTH_HZ < bandwidth < MAX_BANDWIDTH_HZ:
            detection_count += 1
            peak_freq = freqs[np.argmax(power)]

            # Conferma più rilevazioni consecutive e rispetto cooldown
            if detection_count >= MIN_PEAK_CONFIRMATIONS and (time.time() - last_detection_time) > COOLDOWN_PERIOD:
                last_detection_time = time.time()
                print(f"[⚠️ ATTIVITÀ RILEVATA] Frequenza: {peak_freq/1e6:.4f} MHz | "
                      f"BW: {bandwidth/1e3:.1f} kHz | Potenza: {max_power:.1f} dB | "
                      f"Soglia: {threshold:.1f} dB | Rumore medio: {noise_floor_avg:.1f} dB")
                detection_count = 0
                stampa_ascii_spectrum(freqs, power, threshold)
                return True

    else:
        detection_count = 0

    # Output per debug (aggiorna in linea)
    clear_terminal()
    print(f"[✓ Normale] Max: {max_power:.1f} dB | Soglia: {threshold:.1f} dB | Rumore: {noise_floor_avg:.1f} dB | Freq: {sdr.center_freq}", end='\r')
    stampa_ascii_spectrum(freqs, power, threshold)
    return False


def main():
    try:

        print(f"\nMonitoraggio VHF su {sdr.center_freq/1e6:.3f} MHz")
        print(f"Soglia margine: {THRESHOLD_MARGIN_DB} dB | BW: {MIN_BANDWIDTH_HZ/1e3}-{MAX_BANDWIDTH_HZ/1e3} kHz\n")
        # Stampa spettro nel terminale (ASCII)

        while True:
            set_freuqneza_sdr()
            samples = sdr.read_samples(1024*256)  # Leggero blocco per elaborare più spesso
            rileva_segnale(samples)
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nInterruzione manuale")
    finally:
        sdr.close()
        print("Dispositivo SDR rilasciato")


if __name__ == "__main__":
    main()
