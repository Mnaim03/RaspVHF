curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

arduino-cli config init
arduino-cli core update-index
arduino-cli core install arduino:avr  # Per schede come Arduino UNO