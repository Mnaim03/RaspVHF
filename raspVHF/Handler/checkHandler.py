from mainHandler import *

class OldInput:
    oldFrequence = 0
    oldHz = ''
    oldAnomalia = False

    def __init__(self):
        self.oldFrequence = get_frequence_num()
        self.oldHz = get_frequence_hz()
        self.oldAnomalia = get_anomalia()
        return

    def checkOld(self):
        if (self.oldAnomalia != get_anomalia()) or (self.oldFrequence != get_frequence_num()) or (self.oldHz != get_frequence_hz()):
            self.__init__()
            return True
        return False


