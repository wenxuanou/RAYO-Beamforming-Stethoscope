#include <SPI.h>

//Conections:
//Mega 2560 - 50 (MISO), 51 (MOSI), 52 (SCK), 53 (SS).

int pinDRDY_not = 2; //GPIO 2 detect DRDY_not from ADC, interrupt 

int8_t buffer;  //32 bits of data
uint8 size = 3;   //number of bytes


SPI.transfer(&buffer, size);
void setup() {
  // put your setup code here, to run once:

  int spiFreq = 27000000; //Frequency be 27MHz
  SPISettings mySettting(spiFreq, MSBFIRST, SPI_MODE0);
  SPI.beginTransaction(mySettings); 

  pinMode(pinDRDY_not,INPUT);
  attachInterrupt(digitalPinToInterrupt(pinDRDY_not), readBit(), FALLING);

}

void loop() {
  // put your main code here, to run repeatedly:
}

void readBit(){
  
}
