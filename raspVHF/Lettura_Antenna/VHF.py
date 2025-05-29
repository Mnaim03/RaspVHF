from rtlsdr import RtlSdr
import numpy as np
import time
from collections import deque

global power
global freqs
global threshold

# Configurazione SDR
sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 144.39e6
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
                return True

    else:
        detection_count = 0

    # Output per debug (aggiorna in linea)
    print(f"[✓ Normale] Max: {max_power:.1f} dB | Soglia: {threshold:.1f} dB | Rumore: {noise_floor_avg:.1f} dB", end='\r')
    return False

def stampa_ascii_spectrum(freqs, power, threshold):
    """Stampa una rappresentazione ASCII dello spettro attorno al centro."""
    # Riduci dimensione per il terminale
    step = len(power) // 80
    reduced_power = power[::step][:80]
    reduced_freqs = freqs[::step][:80]

    max_db = max(reduced_power)
    min_db = min(reduced_power)
    scale = 20  # altezza del grafico in righe

    print("\nSpettro semplificato (ASCII):")
    for level in reversed(np.linspace(min_db, max_db, scale)):
        line = ""
        for val in reduced_power:
            if val > level:
                line += "█"
            elif abs(val - threshold) < 0.5:
                line += "-"
            else:
                line += " "
        print(f"{level:6.1f} | {line}")
    print("       +" + "-"*80)
    print("       |" + " " * 35 + "Frequenza →")

def main():
    try:
        print(f"\nMonitoraggio VHF su {sdr.center_freq/1e6:.3f} MHz")
        print(f"Soglia margine: {THRESHOLD_MARGIN_DB} dB | BW: {MIN_BANDWIDTH_HZ/1e3}-{MAX_BANDWIDTH_HZ/1e3} kHz\n")
        # Stampa spettro nel terminale (ASCII)
        stampa_ascii_spectrum(freqs, power, threshold)

        while True:
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
