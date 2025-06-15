from .dataHandler import *

class lastInput:
    lastFrequence = 0
    lastHz = ''
    lastAnomalia = False

    def __init__(self):
        self.oldFrequence = get_frequence_num()
        self.oldHz = get_frequence_hz()
        self.oldAnomalia = get_anomalia()
        return

    def checkChange(self):
        if (bool(self.lastAnomalia) != bool(get_anomalia())) or (int(self.lastFrequence) != int(get_frequence_num())) or (str(self.lastHz) != str(get_frequence_hz())):
            self.__init__()
            return True
        return False


