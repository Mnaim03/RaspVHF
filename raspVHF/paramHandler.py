from mainHandler import get_frequence_num, get_frequence_hz, clear_terminal


class Parameters:
    THRESHOLD_MARGIN_DB = 10  # Margine sopra rumore stimato
    MIN_BANDWIDTH_HZ = 5000
    MAX_BANDWIDTH_HZ = 25000
    MIN_PEAK_CONFIRMATIONS = 3  # Quante rilevazioni consecutive per confermare
    COOLDOWN_PERIOD = 2  # Secondi tra allarmi
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
    sdr.gain = 'auto'
    sdr.sample_rate = 2.4e6

    # Ottieni input
    input_freq = get_frequence_num()
    input_unit = get_frequence_hz()

    # Calcolo finale
    input_hz = unit_to_multiplier(input_unit)
    sdr.center_freq = int(input_freq * input_hz)