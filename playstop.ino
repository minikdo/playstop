int lastMpdState = 0;    // Last MPD state
int buttonState = 0;     // Current state of the button
int lastButtonState = 0; // Previous state of the button
int incomingByte = 0;
String a;

void setup() {
  Serial.begin(9600);
  pinMode(3, INPUT);  // button
  pinMode(4, OUTPUT); // LED
}

void loop() {
  delay(15);
  
  buttonState = digitalRead(3);
  
  delayMicroseconds(40);

  if (buttonState != lastButtonState) {
    if (buttonState == HIGH) {
      if (lastMpdState == 0) {
        Serial.println("PLAY");
        lastMpdState = 1;
      } else {
        Serial.println("STOP");
        lastMpdState = 0;
      }   
    }
  }

  if (Serial.available() > 0) {
    a = Serial.readString(); 
    a.trim();
    if (a.equals("STOP")) {
      digitalWrite(4, LOW);  // LED off
      lastMpdState = 0;
    } else if (a.equals("PLAY")) {
      digitalWrite(4, HIGH); // LED on
      lastMpdState = 1;
    }
  }

  lastButtonState = buttonState;
}
