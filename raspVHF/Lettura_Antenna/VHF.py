from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt
import time

# Configura il ricevitore
sdr = RtlSdr()
sdr.sample_rate = 2.4e6  # 2.4 MHz
sdr.center_freq = 144.39e6  # Frequenza APRS
sdr.gain = 'auto'  # Guadagno fisso consigliato

# Imposta il grafico
plt.ion()
fig, ax = plt.subplots(figsize=(10, 4))
line, = ax.plot([], [])
ax.set_xlabel("Frequenza (MHz)")
ax.set_ylabel("Potenza (dB)")
ax.set_title(f"Monitoraggio RF su {sdr.center_freq / 1e6:.2f} MHz")
ax.grid()


# Funzione di controllo anomalia (semplice)
def is_anomalous(power_db, threshold=-60):
    mean_power = np.mean(power_db)
    return mean_power < threshold


try:
    print(f"In ascolto su {sdr.center_freq / 1e6} MHz... Ctrl+C per interrompere.\n")
    while True:
        samples = sdr.read_samples(256 * 1024)
        window = np.hanning(len(samples))
        samples *= window

        power = np.abs(np.fft.fftshift(np.fft.fft(samples))) ** 2
        power_db = 10 * np.log10(power + 1e-10)  # +1e-10 per evitare log(0)
        freqs = np.linspace(-sdr.sample_rate / 2, sdr.sample_rate / 2, len(power)) + sdr.center_freq

        # Aggiorna il grafico
        line.set_data(freqs / 1e6, power_db)
        ax.set_xlim((freqs[0] / 1e6, freqs[-1] / 1e6))
        ax.set_ylim((np.min(power_db), np.max(power_db)))
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Controllo anomalie
        if is_anomalous(power_db):
            print(f"[!] Anomalia rilevata: segnale basso o assente ({np.mean(power_db):.2f} dB)")

        time.sleep(0.5)  # intervallo tra le letture

except KeyboardInterrupt:
    print("\nInterrotto manualmente. Chiudo SDR...")

finally:
    sdr.close()