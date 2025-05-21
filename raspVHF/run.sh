cd /home/user1/Documents/RaspVHF/raspVHF #cartella del git
git restore . #elimino eventuali cambiamenti fatti dal terminale raspberry
git pull #faccio una pull di aggiornamento

clear #pulisco terminale

#do i permessi ai file
chmod +x CompileArduino.py
chmod +x loopSimulator.py
chmod +x arduino/arduino.ino

#avvio file python
python3 CompileArduino.py
python3 loopSimulator.py
