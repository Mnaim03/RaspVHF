from .dataHandler import *

"""
Classe per monitorare lo stato dell'ultima configurazione del sistema.

Memorizza:
- La frequenza attuale in formato numerico (intero).
- La frequenza attuale in formato stringa (Hz).
- Lo stato dell'anomalia (True/False) al momento dell'istanziazione.

Utilizzata per verificare se vi sono cambiamenti nei parametri monitorati 
rispetto all'ultima lettura registrata.
"""
class lastInput:
    """
    Inizializza l'oggetto salvando lo stato corrente dei parametri:
    - Frequenza (numero e stringa)
    - Stato di anomalia
    """
    def __init__(self):
        self.lastFrequence = int(get_frequence_num())
        self.lastHz = str(get_frequence_hz())
        self.lastAnomalia = str(get_anomalia())

    def update(self):
        self.lastFrequence = int(get_frequence_num())
        self.lastHz = str(get_frequence_hz())
        self.lastAnomalia = str(get_anomalia())

    """
    Verifica se c'è stato un cambiamento rispetto ai parametri salvati:
    - Frequenza numerica
    - Frequenza in Hz
    - Stato di anomalia

    Se è stato rilevato un cambiamento, aggiorna internamente i valori
    memorizzati richiamando il costruttore.
        
    Restituisce:
    - True se è stato rilevato un cambiamento.
    - False altrimenti.
    """
    def checkChange(self):
        if (
                self.lastAnomalia != str(get_anomalia()) or
                self.lastFrequence != int(get_frequence_num()) or
                self.lastHz != str(get_frequence_hz())
        ):
            self.update()
            return True
        return False

    """
    Verifica se c'è stato un cambiamento rispetto ai parametri salvati:
    - Frequenza numerica
    - Frequenza in Hz

    Se è stato rilevato un cambiamento, aggiorna internamente i valori
    memorizzati richiamando il costruttore.

    Restituisce:
    - True se è stato rilevato un cambiamento.
    - False altrimenti.
    """
    def checkFrequence(self):
        frequence = int(get_frequence_num())
        hz = str(get_frequence_hz())
        if (
                self.lastFrequence != frequence or
                self.lastHz != hz
        ):
            self.lastFrequence = frequence
            self.lastHz = hz
            return True
        return False

    """
    Controlla se lo stato di anomalia è cambiato rispetto all'ultima lettura.

    Restituisce:
    - True se lo stato di anomalia è cambiato.
    - False altrimenti.
    """
    def checkAnomalia(self):
        anomalia = str(get_anomalia())
        if  self.lastAnomalia != anomalia :
            self.lastAnomalia = anomalia
            return True
        return False
