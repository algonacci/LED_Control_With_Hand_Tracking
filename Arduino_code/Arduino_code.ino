#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);

String data_serial_receive;
const int relay = 13;

void setup() {
  Serial.begin(57600);
  pinMode(relay, OUTPUT);
  digitalWrite(relay, HIGH);
  

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Face Recognition");
  lcd.setCursor(5, 1);
  lcd.print("System");
  delay(2000);
}

void loop() {
   if (Serial.available() > 0) {
    data_serial_receive = Serial.readStringUntil('\n');
   
    if(data_serial_receive == "1") {
      digitalWrite(relay, LOW);
      lcd.clear();
      lcd.setCursor(1, 0);
      lcd.print("WAJAH DIKENALI");
      lcd.setCursor(1, 1);
      lcd.print("Silahkan Masuk");
      delay(100);
    }
    if(data_serial_receive == "0") {
      digitalWrite(relay, HIGH);
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Memindai Wajah..");
      lcd.setCursor(0, 1);
      lcd.print("Hadap ke kamera");
      delay(100);
    }
  }
}
