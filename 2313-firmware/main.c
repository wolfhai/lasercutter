#include <avr/io.h>
#include <avr/interrupt.h>

#define WS 7
static unsigned char step_0=0;
static unsigned char step_1=0;
unsigned char fs[8]= { 9, 1, 5, 4, 6, 2, 10, 8};

ISR (INT0_vect)
{
    if (PIND & (1<<PD4))
    {
        if (step_0++ == WS)
            step_0=0;
    }
    else if (step_0-- == 0)
        step_0=WS;
    PORTB = fs[step_0] | (fs[step_1]<<4);
}

ISR (INT1_vect)
{
    if (PIND & (1<<PD5))
    {
        if (step_1++ == WS)
            step_1=0;
    }
    else if (step_1-- == 0)
        step_1=WS;
    PORTB = fs[step_0] | (fs[step_1]<<4);
}


int main(void)
{
    DDRB = 255;
    DDRD = 0;
    PORTB = 0;
    PORTD |= (1<<PD0) | (1<<PD2) | (1<<PD3) | (1<<PD4) | (1<<PD5);
    GIMSK |= (1<<INT0)| (1<<INT1);
    MCUCR |= (1<<ISC00) | (1<<ISC01) | (1<<ISC10) | (1<<ISC11);

    sei();
    while(1)
        if (PIND & (1<<PD0))
            PORTB=0;
}
