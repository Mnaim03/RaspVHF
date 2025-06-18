import numpy as np
from .dataHandler import get_frequence_num, get_frequence_hz
from scipy.signal import iirnotch, lfilter #passa bada per frequenze fisse

class Parameters:
    THRESHOLD_MARGIN_DB = 10  # Margine sopra rumore stimato
    MIN_BANDWIDTH_HZ = 5000
    MAX_BANDWIDTH_HZ = 25000
    MIN_PEAK_CONFIRMATIONS = 0.5  # Quante rilevazioni consecutive per confermare
    COOLDOWN_PERIOD = 3  # Secondi tra allarmi
    NOISE_ESTIMATION_WINDOW = 20  # Numero di blocchi per stimare rumore

def unit_to_multiplier(unit):
    unit = unit.lower()
    return {
        "hz": 1,
        "khz": 1_000,
        "mhz": 1_000_000,
        "ghz": 1_000_000_000
    }.get(unit, 1)  # default = 1 Hz

def set_freuqneza_sdr(sdr):

    # Ottieni input
    input_freq = get_frequence_num()
    input_unit = get_frequence_hz()

    # Calcolo finale
    input_hz = unit_to_multiplier(input_unit)
    sdr.center_freq = int(input_freq * input_hz)

    sdr.gain = 'auto'
    sdr.sample_rate = 1 * input_hz

def apply_notch_filter(samples, sample_rate, Q=30):
    try:
        notch_freq_relative = 0  # 0 Hz = centro della banda base dopo il downmixing

        # Normalizza rispetto a Nyquist (sample_rate/2)
        w0 = 0.01 if notch_freq_relative == 0 else abs(notch_freq_relative) / (sample_rate / 2)

        if not (0 < w0 < 1):
            raise ValueError(f"w0 fuori range: {w0}")

        b, a = iirnotch(w0, Q)
        return lfilter(b, a, samples)

    except Exception as e:
        print(f"[!] Errore filtro notch: {e}")
        return samples  # Se errore, restituisce i campioni non filtrati

def stampa_ascii_spectrum(freqs, power, threshold):
    """Stampa una rappresentazione ASCII dello spettro centrata sulla soglia."""
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