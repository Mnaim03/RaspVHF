cd /home/user1/Documents/RaspVHF/raspVHF
git restore . #elimino eventuali cambiamenti fatti dal terminale raspberry
git pull #faccio una pull di aggiornamento

#do i permessi ai file
chmod +x CompileArduino.py
chmod +x loopSimulator.py
chmod +x arduino/arduino.ino

#avvio file python
python3 RunArduino.py
python3 loopSimulator.py
