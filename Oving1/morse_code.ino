
const int redPin = 10;
const int yellowPin = 9; 
const int greenPin = 8;
const int dotSignal = 0;
const int dashSignal = 1;
const int letterPauseSignal = 2;
const int wordPauseSignal = 3;
const int buttonPin = 12;
int buttonState;

const int T = 500;
const int dotDurationMax = T;
const int letterPause = 3*T;
const int wordPause = 7*T;
int previousButtonState; 

long buttonChangeTime;
long buttonRelease;
boolean hasSentSomething;
boolean hasSentWord;

void setup() {
  Serial.begin(9600);
  pinMode(redPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(buttonPin, INPUT);
  digitalWrite(redPin, HIGH);
  digitalWrite(greenPin, HIGH);
  delay(1000);
  digitalWrite(redPin, LOW);
  digitalWrite(greenPin, LOW);
  previousButtonState = LOW;
  buttonState = LOW;
  hasSentSomething = false;
  hasSentWord = false;
}

void loop() {
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH && previousButtonState == LOW) {
    // finner tiden der knappen blir trykket inn
      previousButtonState = HIGH;
      buttonChangeTime = millis();
      // sjekker om pausen fra forrige trykk tilsvarer bokstavpause eller ordpause
      long timeSinceLastSignal = millis() - buttonRelease;
      if (hasSentSomething){
         if (timeSinceLastSignal < wordPause && timeSinceLastSignal > letterPause){
            Serial.print(letterPauseSignal);
            delay(20);
           }
          else if (timeSinceLastSignal > wordPause){
            hasSentWord = true;
            Serial.print(wordPauseSignal);
            delay(20);
          }
        hasSentSomething = false;
      }
  }
  // sjekker om tidsintervallet der knappen er trykket inn tilsvarer dot eller dash
  if (buttonState == LOW){
    if (previousButtonState == HIGH && !hasSentWord){
      previousButtonState = LOW;
      if (millis() - buttonChangeTime > dotDurationMax){
         Serial.print(dashSignal);
         digitalWrite(greenPin, HIGH);
         delay(200);
         digitalWrite(greenPin, LOW);
        }
      else {
         Serial.print(dotSignal);
         digitalWrite(redPin, HIGH);
         delay(200);
         digitalWrite(redPin, LOW);
        }
      // finner tiden der knappen er blitt sluppet
      buttonRelease = millis();
      hasSentSomething = true;
    } 
    delay(10);
  }
}
