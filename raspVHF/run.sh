cd /home/user1/Documents/RaspVHF/raspVHF #path del programma da eseguire

#Aggiorno il programma in caso di modifiche del codice direttamente dalla Repo GitHub
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
sudo chmod 666 /var/www/html/logs.txt

# L’opzione -I (isolated mode) forza Python a ignorare variabili che potrebbero causare problemi
python3 -I -m venv venv
source venv/bin/activate

#avvio file python
python3 main.py

deactivate