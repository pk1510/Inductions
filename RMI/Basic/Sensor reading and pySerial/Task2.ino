int Vpin = A0;
int potVal;
void setup() {
  pinMode(Vpin, INPUT);// put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
   // put your main code here, to run repeatedly:
 if(Serial.available() > 0 && Serial.read() == 'S'){
   while(Serial.read() != 'E'){
     potVal = analogRead(Vpin);
     Serial.println((5./1023.) * potVal);
   }
 }
delay(50); 
}
//connect a wire from 5V to one leg of a 10kohm resistor, connect the other leg to one leg of the photoresistor and connect the photo resistor to the gnd. connect a wire from the first leg of the photoresistor
//to pin A0.The analogRead of that gives the potential drop across it
