#include<avr/io.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define BAUD 9600                           // define baud
#define BAUDRATE ((F_CPU)/(BAUD*16UL)-1)    // set baudrate value for UBRR
float val1, val2, dummy;
unsigned char pot1[] = "dutyCycle = ";
unsigned char pot2[] = "frequency = ";
char res1[40], res2[40];                    // to convert voltages to string
int high, low, mspeedNew, fNew;  // using dummy to round off and low and high for adcl and adch
int mspeedOld = 0;
int fOld = 128;
unsigned long int k=0;
volatile static unsigned int count=2;
volatile static unsigned int arr[3];
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
  PORTC = (1<<PC0)|(1<<PC2); //ADC pins        //A0 and A2 pins
  ADCSRA = 0x87;                             // put your setup code here, to run once:
  DDRD |= (1<<PD5)|(1<<PD7)|(1<<PD4);
  PORTD |= (1<<PD7);
  PORTD &= ~(1<<PD4);
  PORTB |= (1<<PB0)|(1<<PB3);
  TCCR0A |= 0x21;
  OCR0A = 128;
  OCR0B = 0;
  TCNT0 = 0;
  
  TCCR0B |= 0x0B;
  TCCR1A = 0x00;
  TCNT1 = 0;
  TIFR1 |= (1<<ICF1);
  TIMSK1 |= (1<<ICIE1);
  //TCCR1B &= ~(1<<ICES1);
  TCCR1B |= 0xC1;
  sei();
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
   mspeedNew = (low + (high*256))/4;
   if (mspeedNew!=mspeedOld)
      OCR0B = mspeedNew;
   mspeedOld = mspeedNew;   
  if(count==2 && arr)
    val1 = (1 - (arr[1] - arr[0])/(arr[2] - arr[0]))*100;    // find the voltage
    
    dummy = val1*1000;
    val1 = (float)(dummy/1000);               // rounding off
    //Serial.println(val1);
            // we can do the same for %100 but in my simulation i din get any false output.
    
     dtostrf(val1, 20, 3, res1);
    //Serial.println(res1);
  ADMUX=0x42;
    ADCSRA |= (1<<ADSC);
    while(!(ADCSRA & (1<<ADIF)));
    ADCSRA |= (1<<ADIF);
    low = (int)ADCL;
    high = (int)ADCH;
    fNew = (low+high*256)/4;
    if(fNew!=fOld)
      OCR0A = fNew;
    fOld = fNew;
  if(count==2 && arr)
    val2 = F_CPU/(arr[2] - arr[0]) ;
    dummy = val2*1000;
    Serial.println(ICR1);
    val2 = (float)dummy/1000;
    
    
     dtostrf(val2,20,3,res2);
    strcat(res1, "\n");
    strcat(res2, "\n");
    for(int k=0; pot1[k]!=0; k++)          // serial communication
      uart_transmit(pot1[k]); 
    for(int i=0; res1[i]!=0; i++)
      uart_transmit(res1[i]);// put your main code here, to run repeatedly:
    for(int l=0; pot2[l]!=0; l++)
      uart_transmit(pot2[l]);
    for(int j=0;res2[j]!=0; j++)
      uart_transmit(res2[j]);
}
ISR(TIMER1_CAPT_vect){
  Serial.println("a");
  if(count ==2) {
    arr[0] = ICR1;
    TCCR1B = 0x42;
    count=0;
  }
  else if(count == 0){
    arr[1] = ICR1;
    TCCR1B = 0x02;
    count=1;    
  }
  else if(count == 1){
    arr[2] = ICR1;
    count=2;
  }
} 
