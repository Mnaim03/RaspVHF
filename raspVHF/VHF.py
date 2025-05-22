from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt

# Inizializza il ricevitore
sdr = RtlSdr()

# Configura parametri
sdr.sample_rate = 2.4e6      # in Hz
sdr.center_freq = 144.39e6   # frequenza VHF in Hz (es: APRS)
sdr.gain = 'auto'

# Legge 256k campioni
samples = sdr.read_samples(256*1024)

# Chiude la connessione
sdr.close()

# Analisi: Spettro in frequenza
power = np.abs(np.fft.fftshift(np.fft.fft(samples)))**2
freqs = np.linspace(-sdr.sample_rate/2, sdr.sample_rate/2, len(power)) + sdr.center_freq

plt.figure(figsize=(10, 4))
plt.plot(freqs / 1e6, 10*np.log10(power))
plt.xlabel('Frequenza (MHz)')
plt.ylabel('Potenza (dB)')
plt.title('Spettro RF su 144.39 MHz')
plt.grid()
plt.show()