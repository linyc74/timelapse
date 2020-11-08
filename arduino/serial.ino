int laser = 8;
int power;
char ser;
int steps = 80;
int t_on = 100;
int t_off = 900;
int led = 255;


void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT); // Connect pin 8 to CLK+ to send pulse for each step
  pinMode(9, OUTPUT); // Connect pin 9 to CW+ to control direction
                      // Connect GND to CLK- and CW-
  pinMode(11,OUTPUT); // Laser
  pinMode(3,OUTPUT);  // LED
}


void loop() {
  power = (laser * 16) - 1;
  analogWrite(11, power);
  analogWrite(3, led); // Pin 3 is connected to the 0V of LED. So when pin 3 = 5V (i.e. 255) the LED is off; when pin 3 = 0V the LED is on.
  if (Serial.available() > 0) {
    ser = Serial.read();
    if (ser == 51 | ser == 52) {
      if (ser == 51) {digitalWrite(9, HIGH);}
      if (ser == 52) {digitalWrite(9, LOW);}
      for (int i=0; i<=steps; i++) {
        digitalWrite(8, HIGH);
        delayMicroseconds(t_on);
        digitalWrite(8, LOW);
        delayMicroseconds(t_off);
      }
      Serial.write(0);
    }
    if (int(ser) >= 1 & int(ser) <= 16) {
      laser = int(ser);
      Serial.write(0);
    }
    if (int(ser) == 61) {
      for (int i=255; i>=0; i--) { // Tune down pin 3 = Turn on LED
        analogWrite(3, i);
        delay(20); // 20 msec
      }
      led = 0;
      Serial.write(0);
    }
    if (int(ser) == 62) {
      for (int i=0; i<=255; i++) { // Tune up pin 3 = Turn off LED
        analogWrite(3, i);
        delay(6); // 6 msec
      }
      led = 255;
      Serial.write(0);
    }
  }
}
