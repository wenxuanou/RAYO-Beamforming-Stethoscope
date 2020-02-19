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

# Sampling in 2 channels, need to power up corresponding channel on ADC
# Using dynamic sampling mode, erased empty channel
Vref = 2.5
chanNum = 2 
volts = []

def inv_twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = (~val & 0xFFF)  + 1
        # compute negative value
    return val

def readADC(self):
    #results = spi.readbytes(3)
    #value = (results[0] << 16) + (results[1] << 8) + (results[2])
    #hex_vals = (value & 0xFFFFFF)
    #print((inv_twos_comp(value,24)))
    #print(hex(hex_vals))

    #Vref = 2.5
    #volts = (value/(2**23-1))*(2 * Vref)
    
    #print(volts)
    
    ########################################
    #For 2 channel sampling, chanNum = 2
    for count in range(chanNum):
        results = spi.readbytes(3)
        value = (results[0] << 16) + (results[1] << 8) + (results[2])
        value = inv_twos_comp(value, 24) 
        volts[count] = (value/(2**23-1))*(2 * Vref)
        
    tstamp = (time.strftime("%Y %d %b %H.%M.%S"))# Create time stamp
    print(tstamp, "Channel A: ", volts[0], "Channel B: ", volts[1]);

# Setup interrupt listening data r
GPIO.add_event_detect(17, GPIO.FALLING, callback = readADC, bouncetime = 300)

if __name__ == "__main__":
    print("run")
    
    for count in range(chanNum):
        volts.append(0)






