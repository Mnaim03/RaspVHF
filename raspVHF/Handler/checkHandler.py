from .dataHandler import *

class lastInput:
    def __init__(self):
        self.lastFrequence = int(get_frequence_num())
        self.lastHz = str(get_frequence_hz())
        self.lastAnomalia = bool(get_anomalia())

    def checkChange(self):
        print(f"[DEBUG] Anomalia: Last={self.lastAnomalia}, Now={get_anomalia()}")
        if (
            self.lastAnomalia != bool(get_anomalia()) or
            self.lastFrequence != int(get_frequence_num()) or
            self.lastHz != str(get_frequence_hz())
        ):
            self.__init__()
            return True
        return False

