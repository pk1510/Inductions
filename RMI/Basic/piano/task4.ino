

int speakerPin = 10; //pwm pin
int sa =4;
int ma = 5;
int ni = 6;
int up = 2;
int down = 3;  // both of them are interrupts
int frequencies[] = {240, 360, 450};
int currentState[3];
int lastState[] = {1,1,1}; 
int chatterTime = 10;       // after this time the bouncing problem will be solved
unsigned long debounceTime = 0; // waiting till chattertime gets over
int vol =3;                     // default volume is 3
unsigned long T;
void setup() {
  pinMode(speakerPin, OUTPUT);// put your setup code here, to run once:
  pinMode(sa, INPUT);
  pinMode(ma, INPUT);
  pinMode(ni, INPUT);;
  attachInterrupt(digitalPinToInterrupt(up), inc, FALLING);   // call the function inc when the up pin changes value
  attachInterrupt(digitalPinToInterrupt(down), dec, FALLING);
}

void loop() {
  for(int i=0; i<3; i++){
    currentState[i] = digitalRead(i+4);      
    if(currentState[i] != lastState[i]){// checking whether bouncing would have occured
      debounceTime = millis();  
      //reset the timer
    }
    if((millis() - debounceTime) > chatterTime){  //waiting for chatter time to get over
      if(currentState[i] == 0 && lastState[i] == 1){ 
        T = 1000000/frequencies[i];  //time period in ms
        digitalWrite(speakerPin, HIGH);
        delay(floor(T*vol/5));   //adjusting duty cycle for volume
        digitalWrite(speakerPin, LOW);
        delay(floor(T*(5-vol)/5));
      }
      else if(currentState[i] == 0 && lastState[i] == 0) {
        T = 1000/frequencies[i];  //time period in ms
        digitalWrite(speakerPin, HIGH);
        delay(floor(T*vol/5));   //adjusting duty cycle for volume
        digitalWrite(speakerPin, LOW);
        delay(floor(T*(5-vol)/5));
      }
      else if(currentState[i] == 1 && lastState[i] == 0) {
        analogWrite(speakerPin, 0);  //if unpressed 
      }
      lastState[i] = currentState[i];
    }
   }
  
   
}

void inc() {   // use hardware debouncing here because it is of great disadvantage to delay 50 ms inside the isr.
  if(vol<5)
  vol++;
}
void dec() {
  if(vol>0)
  vol--;
}

//connect all the buttons to the pin and other leg of all the buttons to gnd. connect one end of the buzzer to gnd and another leg to a resistor which is in turn connected to the 5V.
// if the switch captures noise due to mechanical defects and non idealities in the switch and makes the circuit complete, misinterpretation occurs. so to overcome this with software, we can wait for sometime say 50ms
// after the switch is pressed. if the sswitch is prolonged to stay in that same state, then it is actually pressed..else it is due to bouncing. 
// another way is using hardware interrupts. if the switch is pressed due to noise, the capacitor gets charged fully but has no time to discharge and hence the circuit iws open and the reading of buttonpin
//is high. else if the switch is pressed by the user. it discharges since there is more time.

// for pins up and down connect a 100nF capacitor where one of its leg is connected to the 5V and other is connected to the gnd. so intially it remains fully charged. so while bouncing, since RC >>> bouncing time, 
//ideally no current flows. so digitalRead(2) wont change value.
