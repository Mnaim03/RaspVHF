
#include <LiquidCrystal.h>

int frequence; //frequnza di lettura
String hz; // misura di hz
int input = -1; // valore dato dal raspberry attraverso python

const int buzz = 4;
const int red = 2, green = 3;
const int rs = 8, en = 9, d4 = 10, d5 = 11, d6 = 12, d7 = 13;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {  
  lcd.begin(16, 2);

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
  lcd.setCursor(0, 0);
  lcd.print("f = ");
  lcd.print(frequence);
  lcd.print(" ");
  hz.trim();
  lcd.print(hz);
}

void fxAlert(){
  lcd.setCursor(0, 1);
  lcd.print("Intercettazione");

  digitalWrite(green, LOW);
  digitalWrite(red, HIGH);
  buzzOn();
}

void fxCalm(){
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
  while (!Serial.available()) {
    printWait();
    delay(500); // evito di stamparlo troppe volte
  }


  // Loop principale
  while (true) {
    int lav;

    // Leggo valori da seriale (frequenza + input)

      input = Serial.parseInt();
      frequence = Serial.parseInt();
      hz = Serial.readString();

      while (Serial.available()) Serial.read(); // pulizia

      lcd.clear();
      printFrequenza();

      // Gestione segnali
      if (input == 1) {
        fxCalm();
      } else if (input == 2) {
        fxAlert();
      } else if (input == 3) {
        done();
      }
    }

    while (!Serial.available()) {
        delay(100); // evito di stamparlo troppe volte
    }

  }
}
