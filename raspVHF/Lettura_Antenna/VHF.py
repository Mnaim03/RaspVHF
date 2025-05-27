from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt
import time

# Inizializza SDR
sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 144.39e6
sdr.gain = 30  # Guadagno fisso consigliato

# Imposta grafico
plt.ion()
fig, ax = plt.subplots(figsize=(10, 4))
line, = ax.plot([], [])
ax.set_xlabel("Frequenza (MHz)")
ax.set_ylabel("Potenza (dB)")
ax.set_title(f"Monitoraggio RF su {sdr.center_freq / 1e6:.2f} MHz")
ax.grid()

# Funzione di rilevamento anomalie
def is_anomalous(power_db, threshold=-60):
    mean_power = np.mean(power_db)
    return mean_power < threshold

try:
    print(f"In ascolto su {sdr.center_freq/1e6:.2f} MHz... (Ctrl+C per interrompere)\n")
    while True:
        samples = sdr.read_samples(256*1024)
        samples *= np.hanning(len(samples))  # finestra per ridurre leakage FFT

        power = np.abs(np.fft.fftshift(np.fft.fft(samples)))**2
        power_db = 10 * np.log10(power + 1e-10)  # Evita log(0)
        freqs = np.linspace(-sdr.sample_rate/2, sdr.sample_rate/2, len(power)) + sdr.center_freq

        # Aggiorna grafico
        line.set_data(freqs / 1e6, power_db)
        ax.set_xlim(freqs[0] / 1e6, freqs[-1] / 1e6)
        ax.set_ylim(np.min(power_db), np.max(power_db))
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Log in console
        mean_db = np.mean(power_db)
        max_db = np.max(power_db)
        min_db = np.min(power_db)

        if is_anomalous(power_db):
            print(f"[!] Anomalia: potenza media = {mean_db:.2f} dB — segnale debole o assente")
        else:
            print(f"[OK] Potenza media = {mean_db:.2f} dB | max = {max_db:.2f} | min = {min_db:.2f}")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nInterrotto manualmente. Chiudo SDR...")

finally:
    sdr.close()