import spidev
import time

# Set Transmission

# Configure SPI
byteNum = 24 # 24-bit ADC, 3 byte , 8 channel
spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 1000000 # set 1MHz SPI speed, min 100KHz, max 27MHz
spi.mode = 0b01

try:
    while True:
        #resp = spi.xfer2([0xAA])



        time.sleep(0.0001) # sleep for seconds
    #end while
except KeyboardInterrupt:
# create spi object
# open spi port 0, device (CS) 1
# transfer one byte
# sleep for 0.1 seconds
# Ctrl+C pressed, so...
spi.close() # ... close the port before exit #end try