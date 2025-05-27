from rtlsdr import RtlSdr
import numpy as np
import time

# Inizializza SDR
sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 144.39e6  # Frequenza target in Hz
sdr.gain = 40  # Alta sensibilità

# Parametri soglia
THRESHOLD_DB = -30  # Soglia più bassa per ridurre falsi positivi
MIN_BANDWIDTH_HZ = 5000  # Larghezza di banda minima più piccola
MIN_PEAK_DURATION = 3  # Numero minimo di rilevazioni consecutive per conferma

# Variabili di stato
detection_count = 0
last_detection_time = 0
cooldown_period = 5  # Secondi di attesa dopo una rilevazione


def rileva_segnale_attivo(samples, sdr):
    global detection_count, last_detection_time

    samples *= np.hanning(len(samples))
    spectrum = np.fft.fftshift(np.fft.fft(samples))
    power = 10 * np.log10(np.abs(spectrum) ** 2 + 1e-12)
    freqs = np.linspace(-sdr.sample_rate / 2, sdr.sample_rate / 2, len(power)) + sdr.center_freq

    max_power = np.max(power)
    mean_power = np.mean(power)
    std_power = np.std(power)

    # Calcola soglia dinamica basata sul rumore di fondo
    dynamic_threshold = mean_power + (3 * std_power)
    threshold = max(THRESHOLD_DB, dynamic_threshold)

    if max_power > threshold:
        indices = np.where(power > threshold)[0]
        if len(indices) > 1:
            bandwidth = freqs[indices[-1]] - freqs[indices[0]]
            if bandwidth > MIN_BANDWIDTH_HZ:
                detection_count += 1
                peak_freq = freqs[np.argmax(power)]

                # Richiede multiple rilevazioni consecutive
                if detection_count >= MIN_PEAK_DURATION and time.time() - last_detection_time > cooldown_period:
                    last_detection_time = time.time()
                    print(f"[⚠️  ATTIVITÀ RILEVATA] Frequenza: {peak_freq / 1e6:.4f} MHz | "
                          f"Larghezza: {bandwidth:.0f} Hz | Potenza: {max_power:.2f} dB | "
                          f"SNR: {max_power - mean_power:.2f} dB")
                    return True
                return False

    # Reset conteggio se nessun segnale rilevato
    detection_count = 0
    print(f"[✓ Spettro normale] Picco: {max_power:.2f} dB | Media: {mean_power:.2f} dB | "
          f"Soglia: {threshold:.2f} dB")
    return False


def main():
    try:
        print(f"In ascolto su {sdr.center_freq / 1e6:.2f} MHz per segnali attivi...\n"
              f"Premi Ctrl+C per uscire.\n")
        while True:
            samples = sdr.read_samples(256 * 1024)
            rileva_segnale_attivo(samples, sdr)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nInterrotto manualmente.")
    finally:
        sdr.close()


if __name__ == "__main__":
    main()