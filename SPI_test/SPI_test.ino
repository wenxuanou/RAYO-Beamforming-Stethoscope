#include <SPI.h>

//Conections:
//Mega 2560 - 50 (MISO), 51 (MOSI), 52 (SCK), 53 (SS).

const int pinDRDY_not = 2; //GPIO 2 detect DRDY_not from ADC, interrupt 

int channelCount = 0;
const int channelNum = 6;   //number of bytes,
uint8_t dataBuffer[6];  //32 bit container of 8 bit data, 6 channels


void setup() {
  // put your setup code here, to run once:

  //int spiFreq = 27000000; //Frequency be 27MHz
  int spiFreq = 8000000; // reduce to 8MHz
  SPI.beginTransaction(SPISettings(spiFreq, MSBFIRST, SPI_MODE0)); 

  pinMode(pinDRDY_not,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pinDRDY_not), readBit, FALLING);

  for(int count = 0; count < channelNum; count++){
      dataBuffer[count] = 0x00; 
    }

  Serial.begin(9600); // open the serial port at 9600 bps

}

void loop() {
  // put your main code here, to run repeatedly:
  for(int count = 0; count < channelNum; count++){
    Serial.print(binary2decimal(dataBuffer[count]));
    Serial.print("\t");
    }
    
  Serial.println();
  delay(200);            // delay 200 milliseconds
}

void readBit(){
  for(int count = 2; count >= 0; count--){
      uint8_t data = SPI.transfer(0x00); //Transfer 8 bit data
      dataBuffer[channelCount] |= data << (count * 8);  //Concatenate to 24 bit  
    }

  if(channelCount < channelNum){
    channelCount++; //Move to next channel
  }else{
    channelCount = 0;
    }
}

int binary2decimal(uint8_t input){
    int output;
    uint8_t temp;

    temp = ~input;
    temp += 0x01;

    for(int count = 0; count < 24; count++){
      output += (input & (0x01 << count)) * pow(2,count);
      }
  }
