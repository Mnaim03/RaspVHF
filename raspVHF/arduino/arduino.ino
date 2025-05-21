
#include <LiquidCrystal.h>

int frequence = 157;
int input = 1; // valore dato dal raspberry attraverso python

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
    lcd.print("Attendere... ");

    lcd.setCursor(0, 1);
    lcd.print("Caricamento !");
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
    while(!Serial.available()){ // attesa valore seriale
        printWait();
    }

    //fine attesa
    input = Serial.parseInt(); //lettoura porta seriale
    if(input==1){
        fxAlert();
    }else{
        fxCalm();
    }

    delay(1000);
}
