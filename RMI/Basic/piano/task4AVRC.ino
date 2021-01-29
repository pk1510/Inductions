#include<avr/io.h>

#define speakerPin PB1
#define sa PA2
#define re PA3
#define ga PA4
#define up PA5
#define down PA6


int main(){
  DDRB = 0x02;
  DDRA = 0x00;
  PINA |= (1<<sa)|(1<<re)|(1<<ga)|(1<<up)|(1<<down);
  TCNT0 = 0x00;
  OCR0 = 127;
  while(1){
    if(
  }
}
