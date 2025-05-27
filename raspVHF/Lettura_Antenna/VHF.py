from rtlsdr import RtlSdr
import numpy as np
import time

# Configurazione SDR
sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 144.39e6
sdr.gain = 'auto'  # Guadagno automatico per evitare saturazione

# Parametri ottimizzati
THRESHOLD_DB = -20  # Soglia più alta per evitare falsi positivi
MIN_BANDWIDTH_HZ = 5000  # Larghezza minima realistica
MAX_BANDWIDTH_HZ = 25000  # Larghezza massima per segnali VHF
MIN_PEAK_DURATION = 5  # Conferma con più rilevazioni
COOLDOWN_PERIOD = 2  # Secondi tra rilevazioni

# Variabili di stato
detection_count = 0
last_detection_time = 0


def rileva_segnale_attivo(samples):
    global detection_count, last_detection_time

    # FFT con finestra di Hann
    samples *= np.hanning(len(samples))
    spectrum = np.fft.fftshift(np.fft.fft(samples))
    power = 10 * np.log10(np.abs(spectrum) ** 2 + 1e-12)
    freqs = np.linspace(-sdr.sample_rate / 2, sdr.sample_rate / 2, len(power)) + sdr.center_freq

    max_power = np.max(power)
    mean_power = np.mean(power)

    # Soglia dinamica basata sul rumore di fondo
    threshold = max(THRESHOLD_DB, mean_power + 10)

    if max_power > threshold:
        indices = np.where(power > threshold)[0]
        bandwidth = freqs[indices[-1]] - freqs[indices[0]] if len(indices) > 1 else 0

        # Filtra per banda realistiche
        if MIN_BANDWIDTH_HZ < bandwidth < MAX_BANDWIDTH_HZ:
            detection_count += 1
            peak_freq = freqs[np.argmax(power)]

            # Verifica se è una rilevazione valida
            if (detection_count >= MIN_PEAK_DURATION and
                    time.time() - last_detection_time > COOLDOWN_PERIOD):
                last_detection_time = time.time()
                print(f"[⚠️  ATTIVITÀ RILEVATA] Frequenza: {peak_freq / 1e6:.4f} MHz | "
                      f"BW: {bandwidth / 1e3:.1f} kHz | Potenza: {max_power:.1f} dB | "
                      f"SNR: {max_power - mean_power:.1f} dB")
                return True

    # Reset se nessun segnale valido
    detection_count = 0
    print(f"[✓ Normale] Picco: {max_power:.1f} dB | Media: {mean_power:.1f} dB", end='\r')
    return False


def main():
    try:
        print(f"\nMonitoraggio VHF su {sdr.center_freq / 1e6:.3f} MHz")
        print(f"Soglia: {THRESHOLD_DB} dB | BW: {MIN_BANDWIDTH_HZ / 1e3}-{MAX_BANDWIDTH_HZ / 1e3} kHz\n")

        while True:
            samples = sdr.read_samples(1024 * 1024)
            rileva_segnale_attivo(samples)
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nInterruzione manuale")
    finally:
        sdr.close()
        print("Dispositivo SDR rilasciato")


if __name__ == "__main__":
    main()