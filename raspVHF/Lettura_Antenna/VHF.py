from rtlsdr import RtlSdr
import numpy as np
import time

# Inizializza SDR
sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 144.39e6  # Frequenza target in Hz
sdr.gain = 40  # Alta sensibilità

# Parametri soglia
THRESHOLD_DB = -40
MIN_BANDWIDTH_HZ = 10000

def rileva_segnale_attivo(samples, sdr):
    samples *= np.hanning(len(samples))
    spectrum = np.fft.fftshift(np.fft.fft(samples))
    power = 10 * np.log10(np.abs(spectrum)**2 + 1e-12)
    freqs = np.linspace(-sdr.sample_rate/2, sdr.sample_rate/2, len(power)) + sdr.center_freq

    max_power = np.max(power)
    if max_power > THRESHOLD_DB:
        indices = np.where(power > THRESHOLD_DB)[0]
        if len(indices) > 1:
            bandwidth = freqs[indices[-1]] - freqs[indices[0]]
            if bandwidth > MIN_BANDWIDTH_HZ:
                peak_freq = freqs[np.argmax(power)]
                print(f"[⚠️  ATTIVITÀ RILEVATA] Frequenza: {peak_freq/1e6:.4f} MHz | Larghezza: {bandwidth:.0f} Hz | Potenza: {max_power:.2f} dB")
                return
    print(f"[✓ Connessione normale] Picco massimo: {max_power:.2f} dB — Nessuna attività anomala")

try:
    print(f"In ascolto su {sdr.center_freq/1e6:.2f} MHz per segnali attivi...\nPremi Ctrl+C per uscire.\n")
    while True:
        samples = sdr.read_samples(256*1024)
        rileva_segnale_attivo(samples, sdr)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nInterrotto manualmente.")
finally:
    sdr.close()