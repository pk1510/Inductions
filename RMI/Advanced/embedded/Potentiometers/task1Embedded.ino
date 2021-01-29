#include<avr/io.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define BAUD 9600                           // define baud
#define BAUDRATE ((F_CPU)/(BAUD*16UL)-1)    // set baudrate value for UBRR
float val1, val2;
unsigned char pot1[] = "pot1voltage = ";
unsigned char pot2[] = "pot2voltage = ";
char res1[10], res2[10];                    // to convert voltages to string
int high, low, dummy;                       // using dummy to round off and low and high for adcl and adch


void uart_transmit (unsigned char c)
{
  
  while(!(UCSR0A & (1<<UDRE0)));            // wait till previous transmission is done. UDRE0 will be set to 1 if previous transmission is done
  UDR0 = c;
}

int main() {
  
  //Serial.begin(9600);
  unsigned char ubrr = BAUDRATE;
  UBRR0H = ubrr>>8;                          // setting 9600 baud rate
  UBRR0L = ubrr;
  UCSR0C = 0x86;   
  UCSR0B = (1<<TXEN0);
  PORTC = (1<<PC0)|(1<<PC2); //ADC pins        //A0 and A2 pins
  ADCSRA = 0x87;                                //clk/128 for better accuracy and enabling adc
  
  while(1) {
    ADMUX = 0x40;  //pin ADC0 and avcc with aref connected to capacitor
    ADCSRA |= (1<<ADSC);
    while(!(ADCSRA & (1<<ADIF)));
    ADCSRA |= (1<<ADIF);
    low = (int)ADCL;       // ADCH high is stored in buffer
    //Serial.println(low);
    high = (int)ADCH;    // high = buffer
    //Serial.println(high);
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
    //sprintf(res1, "voltage across pot1 = %s \n", res1);
    ADMUX = 0x42;
    ADCSRA |= (1<<ADSC);
    while(!(ADCSRA & (1<<ADIF)));
    ADCSRA |= (1<<ADIF);
    low = (int)ADCL;
    high = (int)ADCH;
    val2 = (low + high*256)*5.000/1023.000 ;
    dummy = val2*1000;
    val2 = (float)dummy/1000;  
    if(dummy%10 == 0)
      dtostrf(val2, 8, 2, res2);
    else
      dtostrf(val2, 8, 3, res2);
    strcat(res2, "\n");
    //sprintf(res2, "voltage across pot2 = %f \n", res2);

    for(int k=0; pot1[k]!=0; k++)          // serial communication
      uart_transmit(pot1[k]); 
    for(int i=0; res1[i]!=0; i++)
      uart_transmit(res1[i]);
    //uart_transmit("\n");
    for(int l=0; pot2[l]!=0; l++)
      uart_transmit(pot2[l]);
    for(int j=0;res2[j]!=0; j++)
      uart_transmit(res2[j]);
    //uart_transmit("\n");
    
    
  }
}  
