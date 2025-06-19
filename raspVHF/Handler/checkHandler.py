from .dataHandler import *

class lastInput:
    def __init__(self):
        self.lastFrequence = int(get_frequence_num())
        self.lastHz = str(get_frequence_hz())
        self.lastAnomalia = get_anomalia()

    def checkChange(self):
        if (
            self.lastAnomalia != get_anomalia() or
            self.lastFrequence != int(get_frequence_num()) or
            self.lastHz != str(get_frequence_hz())
        ):
            self.__init__()
            return True
        return False

    def checkAnmolia(self):
        if  self.lastAnomalia != get_anomalia() :
            return True
        return False
