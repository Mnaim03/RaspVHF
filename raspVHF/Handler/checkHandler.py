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
        if (self.lastAnomalia != get_anomalia()) or (self.lastFrequence != get_frequence_num()) or (self.lastHz != get_frequence_hz()):
            self.__init__()
            return True
        return False


