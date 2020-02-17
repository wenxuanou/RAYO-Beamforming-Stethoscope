# spidev test

# Raspberry Pi 4:
# clock input: Pin 23[SCLK0/GPIO #11]
# MISO: Pin 21 [MISO0/GPIO #9]
# MOSI: Pin 19 [MOSI0/GPIO #10]
# Chip select: Pin 26 [CS1]

import spidev
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    

spi = spidev.SpiDev()
spi.open(0, 0) # bus number, device number
spi.max_speed_hz = 7800000 # up to 125000000Hz = 125.0 MHz
spi.mode = 0b10 # clock polarity and phase (0b00 - 0b11)
spi.no_cs = True 



def inv_twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = (~val & 0xFFF)  + 1
        # compute negative value
    return val

def readADC(self):
    #resp = spi.xfer2([0,0,0])
    results = spi.readbytes(3)
    value = (results[0] << 16) + (results[1] << 8) + (results[2])
    hex_vals = (value & 0xFFFFFF)
    print((inv_twos_comp(value,24)))
    #print(hex(hex_vals))
    
    ##if value > 2**23:
       #value = 2**23 - value
        

    ##Vref = 2.5
    #volts = Vref*value/2**23
    
    ##print(volts)
    
    #print(bin(results[0] << 16))
    #print(results[1])
    #print(results[2])
    #print(resp[0])
    #print(resp[1])
    #print(resp[2])

   
#if __name__ == "__main__":

GPIO.add_event_detect(17, GPIO.FALLING, callback = readADC, bouncetime = 300)




