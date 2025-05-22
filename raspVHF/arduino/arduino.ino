
#include <LiquidCrystal.h>

int frequence = 157;
int input = -1; // valore dato dal raspberry attraverso python
int flag_firstRun = false; //verifica se effittivamente è il primo avvio del raspberry

const int buzz = 4;
const int red = 2, green = 3;
const int rs = 8, en = 9, d4 = 10, d5 = 11, d6 = 12, d7 = 13;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {  
  lcd.begin(16, 2);  
  lcd.print("hello, world!");

  pinMode(buzz, OUTPUT);
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
}

void printWait() {
  lcd.clear(); // pulisce lo schermo
  lcd.setCursor(0, 0);
  lcd.print("___Attendere____");

  lcd.setCursor(0, 1);
  lcd.print("___Caricamento__");

  digitalWrite(red, HIGH);
  digitalWrite(green, HIGH);
}

void printFrequenza(){
  lcd.clear(); // pulisce lo schermo

  lcd.setCursor(0, 0);
  lcd.print("f = ");
  lcd.print(frequence);
  lcd.print(" Hz");
}

void fxAlert(){
  printFrequenza();
  lcd.setCursor(0, 1);
  lcd.print("Intercettazione");

  digitalWrite(green, LOW);
  digitalWrite(red, HIGH);
  buzzOn();
}

void fxCalm(){
  printFrequenza();
  lcd.setCursor(0, 1);
  lcd.print("No Anomalie");

  digitalWrite(red, LOW);
  digitalWrite(green, HIGH);
}

void done(){
    digitalWrite(red, LOW);
    digitalWrite(green, LOW);

    lcd.clear(); // pulisce lo schermo
    lcd.setCursor(0, 0);
    lcd.print("______FINE______");
    lcd.print(frequence);
    lcd.setCursor(0, 1);
    lcd.print("___RICEZIONE____");

    digitalWrite(red, HIGH);
    digitalWrite(green, HIGH);
}

void buzzOn(){
  digitalWrite(buzz, HIGH); // suona 1
  delay(250);
  digitalWrite(buzz, LOW);  // silenzio
  delay(250);
  digitalWrite(buzz, HIGH); // suona 2
  delay(250);
  digitalWrite(buzz, LOW);  // silenzio
  delay(250);
  digitalWrite(buzz, HIGH); // suona 3
  delay(150);
  digitalWrite(buzz, LOW);  // silenzio
  delay(150);
  digitalWrite(buzz, HIGH); // suona 4
  delay(150);
  digitalWrite(buzz, LOW);  // silenzio
}


void loop() {
  Serial.begin(9600);

  // Primo avvio: mostra "Attendere" finché non c'è input
  while (!Serial.available() && flag_firstRun == false) {
    printWait();
    delay(500); // evito di stamparlo troppe volte
  }

  int lav;
  do {

    frequence = Serial.parseInt(); //leggo frequenza
    lav = Serial.parseInt(); // legge il numero segnale
    // svuota eventuali caratteri extra (come \n o spazi)
    while (Serial.available()) Serial.read();

  } while (lav == input || lav == 0 && !flag_firstRun); // evita di ripetere se è lo stesso

  input = lav;

  if (input == 1) {
    fxCalm();
  } else if (input == 2) {
    fxAlert();
  } else if (input == 3) {
    done();
  }

  flag_firstRun = true;
}
