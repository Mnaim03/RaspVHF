import numpy as np
from .dataHandler import get_frequence_num, get_frequence_hz

"""
Modulo per la gestione dei parametri VHF e configurazione dell'SDR.

Include:
- Classe Parameters per definire i parametri di rilevamento.
- Funzione per convertire unità di misura frequenza.
- Funzione per impostare frequenza e configurazione base dell'SDR.
- Funzione per stampa ASCII dello spettro.
"""
class Parameters:
    def __init__(self):
        """
        Contenitore per i parametri configurabili della rilevazione VHF.

        Attributi:
        - THRESHOLD_MARGIN_DB: margine in dB sopra il rumore stimato.
        - MIN_BANDWIDTH_HZ / MAX_BANDWIDTH_HZ: banda minima e massima per considerare un segnale valido.
        - MIN_PEAK_CONFIRMATIONS: numero minimo di rilevazioni consecutive per confermare l'anomalia.
        - COOLDOWN_PERIOD: tempo minimo in secondi tra due allarmi.
        - NOISE_ESTIMATION_WINDOW: numero di finestre per stimare il rumore medio.
        """
        self.THRESHOLD_MARGIN_DB = 20
        self.MIN_BANDWIDTH_HZ = 2
        self.MAX_BANDWIDTH_HZ = 25
        self.MIN_PEAK_CONFIRMATIONS = 1
        self.COOLDOWN_PERIOD = 0.5
        self.NOISE_ESTIMATION_WINDOW = 10

"""
Converte una stringa di unità di frequenza (Hz, kHz, MHz, GHz) nel corrispondente moltiplicatore numerico.

Parametri:
- unit: stringa dell'unità (case-insensitive).

Restituisce:
- Moltiplicatore intero da applicare alla frequenza.
"""
def unit_to_multiplier(unit):
    unit = unit.lower()
    return {
        "hz": 1,
        "khz": 1_000,
        "mhz": 1_000_000,
        "ghz": 1_000_000_000
    }.get(unit, 1)  # default = 1 Hz

"""
Imposta la frequenza centrale, guadagno e sample rate del ricevitore SDR.
Utilizza le impostazioni correnti lette dalla configurazione (frequenza e unità).

Parametri:
- sdr: oggetto SDR da configurare (es. RTL-SDR).
"""
def set_freuqneza_sdr(sdr):

    # Ottieni input
    input_freq = get_frequence_num()
    input_unit = get_frequence_hz()

    # Calcolo finale
    input_hz = unit_to_multiplier(input_unit)
    sdr.center_freq = int(input_freq * input_hz)

    sdr.gain = 'auto'
    sdr.sample_rate = 2.4 * input_hz

"""
Stampa su terminale una rappresentazione ASCII dello spettro di potenza.

Parametri:
- freqs: array delle frequenze (non usato direttamente qui).
- power: array dei valori di potenza.
- threshold: soglia di riferimento in dB per la visualizzazione.

Il grafico ASCII è centrato attorno alla soglia e ridotto a 80 colonne.
"""
def stampa_ascii_spectrum(freqs, power, threshold):
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