cd /home/user1/Documents/RaspVHF/raspVHF #cartella del git
git restore . #elimino eventuali cambiamenti fatti dal terminale raspberry
git pull #faccio una pull di aggiornamento

clear #pulisco terminale

#do i permessi ai file
chmod +x CompileArduino.py
chmod +x mainHandler.py
chmod +x paramHandler.py
chmod +x arduino/arduino.ino

sudo chmod 666 /var/www/html/outputData
sudo chmod 666 /var/www/html/inputData


python3 -m venv venv
source venv/bin/activate

#avvio file python
# python3 CompileArduino.py
sudo python3 mainVHF.py #sudo perchè va a scrivere nei file di apache
