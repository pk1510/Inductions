#include<math.h>
int spin=9; //speedpin shld be squiggly
int dir1 = 2;
int dir2 = 12; // used for direction control
int potPin = A0;
int readVal;

void setup() {
  pinMode(spin, OUTPUT);// put your setup code here, to run once:
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(potPin, INPUT);
  Serial.begin(9600);
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, LOW);
}

void loop() {
  readVal = analogRead(potPin);// put your main code here, to run repeatedly:
  analogWrite(spin, floor(readVal/4));
  
}
// connect the ground of power supply and ground of arduino to the common ground. pins in L293D.. 1-EN1 2-IN1 3-OUT1 4-0V 5-0V 6-OUT2 7-IN2 8-+Vmotor same on the right side.. so we can control 2 motors
// connect the +Vmotor and 0V to power supply rails. connect EN1 to a squigly of arduino which is used for speed control. its values range from 0-255. connect In1 and In2 to digital pins which are used for direction
// connect red wire of motor to out 1 and black wire of motor to out 2.  

// if the dc motor has some starting trouble we can kick start it by doing analogWrite(spin, 255) ; delay(30); and then operate it in the operating range by changing the equation.

// connect centre tap of potentiometer to A0
