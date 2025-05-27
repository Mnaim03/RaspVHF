from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt
import time

# Configura ricevitore
sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 144.39e6
sdr.gain = 40  # alto guadagno per rilevare meglio

# Imposta plot
plt.ion()
fig, ax = plt.subplots(figsize=(10, 4))
line, = ax.plot([], [])
ax.set_title("Monitoraggio interferenze attive / jamming")
ax.set_xlabel("Frequenza (MHz)")
ax.set_ylabel("Potenza (dB)")
ax.grid()

# Parametri soglia
THRESHOLD_JAMMER_DB = -40  # se supera questa soglia = possibile jamming
JAMMER_BANDWIDTH_HZ = 10000  # se ampiezza del segnale anomalo è > 10 kHz


def detect_jammer(power_db, freqs):
    max_power = np.max(power_db)
    if max_power > THRESHOLD_JAMMER_DB:
        peak_idx = np.argmax(power_db)
        peak_freq = freqs[peak_idx]

        # Conta quanto largo è il picco sopra soglia
        high_power_indices = np.where(power_db > THRESHOLD_JAMMER_DB)[0]
        if len(high_power_indices) > 1:
            bandwidth = (freqs[high_power_indices[-1]] - freqs[high_power_indices[0]])
            if bandwidth > JAMMER_BANDWIDTH_HZ:
                return True, peak_freq, bandwidth, max_power
    return False, None, None, None


try:
    print(f"In ascolto su {sdr.center_freq / 1e6:.2f} MHz per jamming/interferenze attive...\n")
    while True:
        samples = sdr.read_samples(256 * 1024)
        samples *= np.hanning(len(samples))

        power = np.abs(np.fft.fftshift(np.fft.fft(samples))) ** 2
        power_db = 10 * np.log10(power + 1e-12)
        freqs = np.linspace(-sdr.sample_rate / 2, sdr.sample_rate / 2, len(power)) + sdr.center_freq

        # Aggiorna grafico
        line.set_data(freqs / 1e6, power_db)
        ax.set_xlim(freqs[0] / 1e6, freqs[-1] / 1e6)
        ax.set_ylim(np.min(power_db), np.max(power_db))
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Rilevazione jammer
        jammer_detected, freq, bw, pwr = detect_jammer(power_db, freqs)
        if jammer_detected:
            print(f"[⚠️  JAMMER RILEVATO] Freq = {freq / 1e6:.4f} MHz | BW = {bw:.0f} Hz | Potenza = {pwr:.2f} dB")
        else:
            print(f"[OK] Nessuna interferenza rilevata ({np.max(power_db):.2f} dB picco)")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Interrotto manualmente. Chiudo SDR...")
finally:
    sdr.close()