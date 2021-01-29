#include<avr/io.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define BAUD 9600                           // define baud
#define BAUDRATE ((F_CPU)/(BAUD*16UL)-1)    // set baudrate value for UBRR
float val1, val2;
unsigned char pot1[] = "pot1voltage = ";
//unsigned char pot2[] = "pot2voltage = ";
char res1[10], res2[10];                    // to convert voltages to string
int high, low, dummy, mspeedNew;                       // using dummy to round off and low and high for adcl and adch
int mspeedOld = 0;

void uart_transmit (unsigned char c)
{
  
  while(!(UCSR0A & (1<<UDRE0)));            // wait till previous transmission is done. UDRE0 will be set to 1 if previous transmission is done
  UDR0 = c;
}

void setup() {
  //Serial.begin(9600);
  unsigned char ubrr = BAUDRATE;
  UBRR0H = ubrr>>8;                          // setting 9600 baud rate
  UBRR0L = ubrr;
  UCSR0C = 0x86;   
  UCSR0B = (1<<TXEN0);
  PORTC = (1<<PC0)|(1<<PC1); //ADC pins        //A0 and A2 pins
  ADCSRA = 0x87;                             // put your setup code here, to run once:
  DDRD |= (1<<PD6)|(1<<PD7)|(1<<PD4);
  PORTD |= (1<<PD7);
  PORTD &= ~(1<<PD4);
  TCCR0A |= 0x81;
  OCR0A = 0;
  TCCR0B |= 0x01;
}

void loop() {
  ADMUX = 0x40;  //pin ADC0 and avcc with aref connected to capacitor
    ADCSRA |= (1<<ADSC);
    while(!(ADCSRA & (1<<ADIF)));
    ADCSRA |= (1<<ADIF);
    low = (int)ADCL;       // ADCH high is stored in buffer
    //Serial.println(low);
    high = (int)ADCH;    // high = buffer
    //Serial.println(high);
   mspeedNew = (low+high*256)/4;
   if (mspeedNew!=mspeedOld)
      OCR0A = mspeedNew;
   mspeedOld = mspeedNew;   
    val1 = (low + (high)*256)*5.00/1023.00;    // find the voltage
    dummy = val1*1000;
    val1 = (float)dummy/1000;               // rounding off
    //Serial.println(val1);
    if(dummy%10 == 0)                     // if my voltage is 2.81, since i gave precision =3 in dtostrf, it prints 28.099. so if dummy is a multiple of 10 the third decimal place is 0.
      dtostrf(val1, 8, 2, res1);          // we can do the same for %100 but in my simulation i din get any false output.
    else
      dtostrf(val1, 8, 3, res1);
    //Serial.println(res1);
    strcat(res1, "\n");
    
    for(int k=0; pot1[k]!=0; k++)          // serial communication
      uart_transmit(pot1[k]); 
    for(int i=0; res1[i]!=0; i++)
      uart_transmit(res1[i]);// put your main code here, to run repeatedly:

}
