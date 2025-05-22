
#include <LiquidCrystal.h>

int frequence = 157;
int input = 1; // valore dato dal raspberry attraverso python
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
}

void printMessage(bool flag) {
  lcd.clear(); // pulisce lo schermo
  lcd.setCursor(0, 0);
    lcd.print("Frequneza = ");
    lcd.print(frequence);

  if(flag==true){
    lcd.setCursor(0, 1);
    lcd.print("Intercettazione");
  } else {
    lcd.setCursor(0, 1);
    lcd.print("No Anomalie");
  }

}

void buzzOn(){
  digitalWrite(buzz, HIGH); // suona
  delay(1000);
  digitalWrite(buzz, LOW);  // silenzio
  delay(500);
}

void fxAlert(){
    printMessage(true);
    digitalWrite(green, LOW);
    digitalWrite(red, HIGH);
    buzzOn();
}

void fxCalm(){
    printMessage(false);
    digitalWrite(red, LOW);
    digitalWrite(green, HIGH);
}

void loop() {
    Serial.begin(9600); //connessione seriale alla porta

    //Attendo il valore seriale al primo avvio
    while(!Serial.available() && flag_firstRun==false){
        printWait();
    }

    //Lascio Schermata fissa finchè non mi ritrovo
    // un'altro valore in ingresso
    while(!Serial.available()){}

    //fine attesa
    input = Serial.parseInt(); //lettoura porta seriale
    if(input==1){
        fxAlert();
    }else{
        fxCalm();
    }

    flag_firstRun = true;
}
