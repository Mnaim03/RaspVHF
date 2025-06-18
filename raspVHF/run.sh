cd /home/user1/Documents/RaspVHF/raspVHF #cartella del git
git restore . #elimino eventuali cambiamenti fatti dal terminale raspberry
git pull #faccio una pull di aggiornamento

clear #pulisco terminale

#do i permessi ai file
chmod +x Handler/vhfHandler.py
chmod +x Handler/dataHandler.py
chmod +x Handler/arduinoHandler.py
chmod +x Handler/checkHandler.py
chmod +x arduino/arduino.ino

#permesso per modificare il file Data nella cartella Apache, web server
sudo chmod 666 /var/www/html/Data

# L’opzione -I (isolated mode) forza Python a ignorare variabili di ambiente che potrebbero stare causando il problema.
python3 -I -m venv venv
source venv/bin/activate

#avvio file python
python3 mainVHF.py #sudo perchè va a scrivere nei file di apache

deactivate