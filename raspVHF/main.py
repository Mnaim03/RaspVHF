from rtlsdr import RtlSdr
import numpy as np
import time
from collections import deque

from Handler.vhfHandler import *
from Handler.checkHandler import *
from Handler.arduinoHandler import *

# Configurazione SDR
sdr = RtlSdr()

#Ogetto Parametri
Parameters = Parameters()

# Code per memorizzare le medie di rumore degli ultimi blocchi
noise_floor_history = deque(maxlen=Parameters.NOISE_ESTIMATION_WINDOW)

#Variabili stato rilevazione: conteggio e distanza temporale tra rilevazioni
detection_count = 0
last_detection_time = 0

#Inzializzo una variabile Arduino
Arduino = start_Arduino()

#Ogetto di lastInput dedicato a scartare segnalazioni continue correnti
checkVHF = lastInput()
checkArduino = lastInput()

"""
Analizza un blocco di campioni SDR per rilevare segnali anomali.

Funzionamento:
- Applica una finestra di Hann ai campioni per ridurre il leakage spettrale.
- Calcola la trasformata di Fourier (FFT) e converte in spettro di potenza (in dB).
- Stima il livello di rumore medio utilizzando una mediana dei valori.
- Calcola una soglia adattiva (rumore medio storico + margine definito).
- Rileva eventuali picchi di potenza superiori alla soglia e ne valuta la larghezza di banda.
- Se il segnale rientra nei parametri di validità (banda compresa tra minimo e massimo), aggiorna il contatore di rilevazioni.
- Se le rilevazioni superano la soglia minima e rispettano il tempo di cooldown,
  conferma l’attività anomala, aggiorna il log e l’interfaccia Arduino.

Restituisce:
- True se viene rilevata un’anomalia valida.
- False in caso contrario.
"""
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
    threshold = noise_floor_avg + Parameters.THRESHOLD_MARGIN_DB

    max_power = np.max(power)
    mean_power = np.mean(power)

    if max_power > threshold:
        indices = np.where(power > threshold)[0]
        if len(indices) > 1:
            bandwidth = freqs[indices[-1]] - freqs[indices[0]]
        else:
            bandwidth = 0

        if (Parameters.MIN_BANDWIDTH_HZ * unit_to_multiplier(get_frequence_hz())) < bandwidth < (Parameters.MAX_BANDWIDTH_HZ * unit_to_multiplier(get_frequence_hz())):
            detection_count += 1
            peak_freq = freqs[np.argmax(power)]

            # Conferma più rilevazioni consecutive e rispetto cooldown
            if (detection_count >= Parameters.MIN_PEAK_CONFIRMATIONS) and (time.time() - last_detection_time) > Parameters.COOLDOWN_PERIOD:

                last_detection_time = time.time()

                clear_terminal()
                print(f"[⚠️ ATTIVITÀ RILEVATA] Frequenza: {peak_freq/1e6:.4f} MHz | "
                      f"BW: {bandwidth/1e3:.1f} kHz | Potenza: {max_power:.1f} dB | "
                      f"Soglia: {threshold:.1f} dB | Rumore medio: {noise_floor_avg:.1f} dB")
                #tampa_ascii_spectrum(freqs, power, threshold)

                detection_count = 0
                set_anomalia(True)
                if checkVHF.checkAnmolia() : update_logs()

                return True

    else:

        # Output per debug (aggiorna in linea)
        clear_terminal()
        print(f"[✓ Normale] Max: {max_power:.1f} dB | Soglia: {threshold:.1f} dB | Rumore: {noise_floor_avg:.1f} dB | Freq: {get_frequence_num()} {get_frequence_hz()} ", end='\r')
        # stampa_ascii_spectrum(freqs, power, threshold)

        detection_count = 0
        set_anomalia(False)

    return False


"""
Ciclo principale di acquisizione e analisi del segnale SDR.

 Funzionamento:
- Aggiorna i parametri correnti dell'Arduino in base alle impostazioni dell'interfaccia.
- Configura e aggiorna continuamente la frequenza del ricevitore SDR.
- Elimina i campioni iniziali obsoleti per evitare dati residui.
- Acquisisce campioni freschi dal ricevitore e li analizza tramite la funzione rileva_segnale().
- Se viene rilevata una variazione significativa, aggiorna l'interfaccia Arduino.
- Gestisce in modo sicuro le interruzioni manuali (KeyboardInterrupt) e rilascia correttamente le risorse.
- Alla chiusura, reimposta lo stato di anomalia a False e libera sia il dispositivo SDR che l'Arduino.

Nota:
- Il ciclo è continuo e gira finché non viene interrotto manualmente.
"""
def main():
    #in caso il file .ino è stato aggiornato, ricompilo il file
    #compile_Arduino()

    #aggioro Arduino con gl'ultimi valori inseriti da interfaccia
    update_arduino(Arduino)
    # Aggiorno costantemente gl'input dell'SDR
    set_freuqneza_sdr(sdr)

    try:
        while True:
            #Verifo eventiali cambiamenti della frequenza in input
            if checkVHF.checkFrequence() :
                set_freuqneza_sdr(sdr)

            #pulisco i sample vecchi generati durante l'esecuzione
            for _ in range(5):
                sdr.read_samples(1024)

            #prendo il sample più recente
            samples = sdr.read_samples(1024 * 64)
            #analizzo sample d'interesse
            rileva_segnale(samples)

            #Verifo eventiali cambiamenti nell'ultima rilevazione
            if checkArduino.checkChange():
                update_arduino(Arduino)

            time.sleep(0.1)

    #Chiusura da tastiera
    except KeyboardInterrupt:
        print("\nInterruzione manuale")
        end_Arduino(Arduino)

    finally:
        sdr.close()
        Arduino.close()
        #Resetto variabile Anomalia al valore di Default, False
        set_anomalia(False)
        print("Dispositivo SDR e Arduino rilasciato")


if __name__ == "__main__":
    main()
