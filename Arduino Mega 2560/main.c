#define F_CPU 16000000UL				//non necessaria
#include <avr/io.h>						//necessaria per gestire PORT e PIN
#include <avr/interrupt.h>				//necessaria per gestire sei()
#include <util/delay.h>
#include <string.h>
#include <avr/wdt.h>

#define MAX 1023
#define USART0_BAUDRATE 500000
long BAUD0 = (F_CPU/16/USART0_BAUDRATE)-1;
long BAUD2 = (F_CPU/16/USART0_BAUDRATE)-1;
volatile uint8_t raspinfo;
volatile uint8_t byte[8];
volatile int k=0;
volatile float speed=0, speed2=0;
volatile uint8_t data;
volatile uint8_t data1;
volatile uint32_t tick=0;
volatile uint32_t delta_tick=0, tick_old = 0, tempo=0, velocita;
volatile uint32_t delta_tick2=0, tick_old2 = 0, tempo2=0, velocita2;
volatile uint32_t delta_tick3=0, tick_old3 = 0, tempo3=0, velocita3;
volatile uint32_t delta_tick4=0, tick_old4 = 0, tempo4=0, velocita4;

float x=0, y=0, z=0, d=0, s=0;
volatile float conta=0, conta2=0, conta3=0, conta4=0;
volatile int impulsi1=0, impulsi2=0, impulsi3=0, impulsi4=0, mediaimpulsi=0, sus=0;
//float Kp=4000.0, Ki=500.0, Kd=00.0;
volatile float Kp=0.8, Ki=0.10, Kd=0.00;
volatile float Kp2=0.8, Ki2=0.10, Kd2=0.0;
volatile float Kp3=0.8, Ki3=0.10, Kd3=0.0;
volatile float Kp4=0.8, Ki4=0.10, Kd4=0.0;
volatile float e=0.0,e_old=0.0, I=0.0,I_old=0.0 ,P=0.0, D=0.0,D_old=0.0, C=0.0;
volatile float e2=0.0,e2_old=0.0, I2=0.0,I2_old=0.0, P2=0.0, D2=0.0,D1_old=0.0, C2=0.0;
volatile float e3=0.0,e3_old=0.0, I3=0.0,I3_old=0.0, P3=0.0, D3=0.0,D2_old=0.0, C3=0.0;
volatile float e4=0.0,e4_old=0.0, I4=0.0,I4_old=0.0, P4=0.0, D4=0.0,D3_old=0.0, C4=0.0;
volatile float a=0.0, a2=0.0, a3=0.0, a4=0.0;
volatile float s1 = 0, s2 = 0 , s3 = 0, s4 = 0;
volatile float Cfermo= 0.0, Cfermo2 = 0.0, Cfermo3 = 0.0, Cfermo4 = 0.0;


void Serial_Init(){
	UBRR0H = (unsigned char)(BAUD0>>8);
	UBRR0L = (unsigned char)BAUD0;
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	UCSR0C = 0b00000110;
}
void Serial_Tx(unsigned char data)
{
	while ( !( UCSR0A & (1<<UDRE0)) );
	UDR0=data;
}
unsigned char Serial_Rx( void )
{
	while ( !(UCSR0A & (1<<RXC0)) );
	return UDR0;
}


void Serial_Send_Int(int32_t num)
{
	if(num<0)
	{
		//Serial_Send_String("-");
		num=-num;
	}
	if(num==0){Serial_Tx('0');}
	else
	{
		char str[32];				// definisce una stringa sulla quale convertire il numero da trasmettere (max 10 cifre)
		char i;						// contatore ciclo
		for(i=0;i<32;i++) str[i]=0; // cancella la stringa
		i=31;
		while (num)
		{
			str[i]=num%10+'0';		// converte il numero da trasmettere in una stringa (dalla cifra meno significativa)
			num/=10;
			i--;
		}
		for (i=0;i<32;i++)			// invia la stringa un carattere alla volta
		if (str[i]) Serial_Tx(str[i]);
	}
}

void Serial2_Init(){
	UBRR2H = (unsigned char)(BAUD2>>8);
	UBRR2L = (unsigned char)BAUD2;
	UCSR2B = (1<<RXEN2)|(1<<TXEN2);
	UCSR2C = 0b00000110;
}

void Serial2_Tx(unsigned char data)
{
	while ( !( UCSR2A & (1<<UDRE2)) );
	UDR2=data;
}

unsigned char Serial2_Rx( void )
{
	while ( !(UCSR2A & (1<<RXC2)) );
	return UDR2;
}
void Serial2N()
{
	Serial2_Tx(13);
	Serial2_Tx(10);
}



ISR (INT2_vect){
	delta_tick = tick - tick_old;
	tick_old = tick;
	tempo = delta_tick*10;
	velocita = 2000000/tempo;
	impulsi1++;
}
ISR(INT3_vect){ //OCR3A
	delta_tick2 = tick - tick_old2;
	tick_old2 = tick;
	tempo2 = delta_tick2*10;
	velocita2 = 2000000/tempo2;
	impulsi2++;
}
ISR(INT4_vect){ //OCR1A
	delta_tick3 = tick - tick_old3;
	tick_old3 = tick;
	tempo3 = delta_tick3*10;
	velocita3 = 2000000/tempo3;
	impulsi3++;
}
ISR(INT5_vect){ //OCR1B
	delta_tick4 = tick - tick_old4;
	tick_old4 = tick;
	tempo4 = delta_tick4*10;
	velocita4 = 2000000/tempo4;
	impulsi4++;
}

ISR(TIMER5_COMPA_vect){
	e=s1-velocita;
	P=e*Kp;
	I=I_old+e*Ki; I_old=I;
	D=(e-e_old)*Kd; e_old=e;
	C=P+I+D;
	
	e2=s2-velocita2;
	P2=e2*Kp2;
	I2=I2_old+e2*Ki2; I2_old=I2;
	D2=(e2-e2_old)*Kd2; e2_old=e2;
	C2=P2+I2+D2;
	
	e3=s3-velocita3;
	P3=e3*Kp3;
	I3=I3_old+e3*Ki3; I3_old=I3;
	D3=(e3-e3_old)*Kd3; e3_old=e3;
	C3=P3+I3+D3;
	
	e4=s4-velocita4;
	P4=e4*Kp4;
	I4=I4_old+e4*Ki4; I4_old=I4;
	D4=(e4-e4_old)*Kd4; e4_old=e4;
	C4=P4+I4+D4;
	
	if((PINF&0b00001000)==0){
		s1=0, s2=0, s3=0, s4=0;
	}
	if(C3>=MAX){
		C3=MAX;
	}
	if(C2>=MAX){
		C2=MAX;
	}
	if(C>=MAX){
		C=MAX;
	}
	if(C4>=MAX){
		C4=MAX;
	}
	
	if((C3)<=0){
		C3=0;
	}
	if(C2<=0){
		C2=0;
	}
	if(C<=0){
		C=0;
	}
	
	if(C4<=0){
		C4=0;
	}
	OCR1A=(uint16_t)(C);
	OCR3A=(uint16_t )(C2);
	OCR1C=(uint16_t )(C3);
	OCR1B=(uint16_t )(C4);
	
	TCNT5=0; //ricorda azzerramento
}
void reset_timer()
{
	// Reset del timer utilizzando il registro appropriato
	TCNT0 = 0;  // Ad esempio, per il timer 0
	// Eventuali altre operazioni di reset necessarie
}
void timer0(){
	TCCR0A = 1<<WGM01;       //modalità ctc
	TCCR0B = 1<<CS00;       //prescaler a 1 (conteggio a 16MHZ)
	TIMSK0 = 1<<OCIE0A;     // interrupt compermatch
	OCR0A = 160;
	//OCR0A = 1600;
}
ISR (TIMER0_COMPA_vect){
	tick++;
}


ISR(USART2_RX_vect)
{
	raspinfo = Serial2_Rx();
}


void av(){
	PORTA=(1<<PA0)| (1<<PA2) | (1<<PA5) | (1<<PA7); //avanti macchinina quattro
	//PORTA = (1<<PA1)|(1<<PA3)|(1<<PA4)|(1<<PA7); //avanti macchinina due
}
void dx(){
	PORTA=(1<<PA0)| (1<<PA2) | (1<<PA4) | (1<<PA6); //destra macchinina quattro
	//PORTA = (1<<PA1)|(1<<PA7)|(1<<PA2)|(1<<PA5); //destra macchinina due
}
void sx(){
	PORTA=(1<<PA1)| (1<<PA3) | (1<<PA5) | (1<<PA7); //sinistra macchinina quattro
	//PORTA = (1<<PA0)|(1<<PA6)|(1<<PA3)|(1<<PA4); //sinistra macchinina due
}
void ind(){
	PORTA=(1<<PA1)| (1<<PA3) | (1<<PA4) | (1<<PA6); //indietro macchinina quattro
	//PORTA = (1<<PA0)|(1<<PA2)|(1<<PA5)|(1<<PA6); //indietro macchinina due
}

int main(void)
{
	Serial_Init();
	Serial2_Init();
	timer0();
	TCCR5A=0;
	TCCR5B=(1<<CS52);
	TIMSK5=(1<<OCIE5A);
	OCR5A=1250; //0.01 sec  1250=20ms
	TCCR1A=(0<<WGM11)|(0<<WGM10)|(1<<COM1A1)|(0<<COM1A0)|(1<<COM1B1)|(0<<COM1B0)|(1<<COM1C1)|(0<<COM1C0);
	TCCR1B=(1<<WGM13)|(0<<WGM12)|(1<<CS12)|(0<<CS11)|(0<<CS10); //mode 8
	TCCR3A=(0<<WGM31)|(0<<WGM30)|(1<<COM3A1)|(0<<COM3A0)|(1<<COM3B1)|(0<<COM3B0)|(1<<COM3C1)|(0<<COM3C0);
	TCCR3B=(1<<WGM33)|(0<<WGM32)|(1<<CS32)|(0<<CS31)|(0<<CS30); //mode 8

	ICR1=1023;
	ICR3=1023;
	//DDRC=0x00;
	DDRA=0xFF;
	//DDRL=0xFF;
	DDRB=(1<<PB5) | (1<<PB6) | (1<<PB7);
	DDRE=(1<<PE3);
	DDRF = 0;
	DDRC=0xFF;
	PORTC=255;
	EICRA=(1<<ISC20)|(1<<ISC21)|(1<<ISC30)|(1<<ISC31);
	EICRB=(1<<ISC40)|(1<<ISC41)|(1<<ISC50)|(1<<ISC51);          //RISING EDGE
	EIMSK=(1<<INT2)|(1<<INT3)|(1<<INT4)|(1<<INT5);  // ABILITA INT0     USANDO sei() richiamo il set enable interrupt
	sei();			//abilitazione generale degli interrupt
	
	while (1){
		while((PINF&0b00001000)!=0){
			//
			//if((tick % 100000) ==0)
			//{
			//Serial_Send_Int(C);
			//Serial_Tx(45);
			//Serial_Send_Int(C2);
			//Serial_Tx(45);
			//Serial_Send_Int(C3);
			//Serial_Tx(45);
			//Serial_Send_Int(C4);
			////Serial_Tx(45);
			//Serial_Tx(13);
			//Serial_Tx(10);
			//}
			raspinfo = Serial2_Rx();
			for(int i=0;i<8;i++){
				byte[i] = (raspinfo >> i) & 1;
			}
			if(byte[7]==1){
				if(byte[4]==1){    //STATO DELLA MACCHININA DEVE ESSERE SEMPRE A 1 TEORICAMENTE
					if(byte[6]==1){
						//richiedi distanza (impulsi)
						mediaimpulsi=0;
						mediaimpulsi = (impulsi4 + impulsi3 + impulsi2 + impulsi1) / 4;
						mediaimpulsi = mediaimpulsi/5;
						if (mediaimpulsi > 240){
							mediaimpulsi = 240;
						}
						uint8_t data1=mediaimpulsi;
						Serial2_Tx(data1);
					}
					if(byte[5]==1){
						//reset distanza (impulsi)
						impulsi1=0; impulsi2=0; impulsi3=0; impulsi4=0;
						mediaimpulsi=0;
					}
					if(byte[3]==1){
						//COPPIA MOTORI  in questo momento funzionano come sS e sD
						s1=s2; s3=s4;
					}
					if(byte[3]==0){
						//COPPIA MOTORI  in questo momento funzionano in diagonale
						s1=s3; s2=s4;
					}
					//byte[2] == byte vuoto da usare come vuoi
					//byte[1] == 1 VERSO COPPIA 1 IN AVANTI DX
					//byte[1] == 0 VERSO COPPIA 1 INDIETRO  DX
					//byte[0] == 1 VERSO COPPIA 2 IN AVANTI SX
					//byte[0] == 0 VERSO COPPIA 2 INDIETRO  SX
					if((byte[1]==1) && (byte[0]==1)){      //avanti
						av();
					}
					if((byte[1]==0) && (byte[0]==0)){      //indietro
						ind();
					}
					if((byte[1]==1) && (byte[0]==0)){       //destra
						dx();
					}
					if((byte[1]==0) && (byte[0]==1)){
						sx();
					}
				}
				else{
					impulsi1=0; impulsi2=0; impulsi3=0; impulsi4=0;
					mediaimpulsi=0;
					s1 = s2 = s3 = s4 = 0;
				}
			}
			if(byte[7]==0){
				
				if(k==0){
					speed=(byte[6]<<6)|(byte[5]<<5)|(byte[4]<<4)|(byte[3]<<3)|(byte[2]<<2)|(byte[1]<<1)|(byte[0]<<0);
					speed=speed*47.24;
					//if (speed == 0){
					//Serial2_Tx(80);
					//}
					s1 = s2 = speed;
					k++;
					}else{
					speed2=(byte[6]<<6)|(byte[5]<<5)|(byte[4]<<4)|(byte[3]<<3)|(byte[2]<<2)|(byte[1]<<1)|(byte[0]<<0);
					speed2=speed2*47.24;
					//if (speed2 == 0){
					//Serial2_Tx(80);
					//}
					s3 = s4 = speed2;
					k=0;
				}
				if(byte[0] ==0 && byte[1]==0 && byte[2]==0 && byte[3] ==0 && byte[4]==0 && byte[5]==0 && byte[6] ==0){
					s1 = s2 = s3 = s4 = 0;
				}
				
				
			}
			for(int i=0;i<8;i++){
				byte[i] = (0 >> i) & 1;
			}
			_delay_ms(1);
			
		}
		s1 = s2 = s3 = s4 = 0;
		Serial2_Tx(80);
		_delay_ms(1);
	}
}


