import spidev
import time
import serial

NUM_CH = 8
adcValues = [0 for i in range(NUM_CH)]


# SPI and Serial port objects
spi = spidev.SpiDev()
spi.open(0,0)
ser = serial.Serial('/dev/ttyUSB0', 57600) #baudrate of arduino motor driver 
time.sleep(0.5)
ser.write(b'xxx') #stop IR polling (from legacy driver firmware)

#################################
#routine for reading analog ports
#################################
def readADC(ch):
   if ( (ch>NUM_CH-1) or (ch<0) ):
      return -1
   r= spi.xfer2([1,(8+ch)<<4,0])
   val = ((r[1]&3)<<8) + r[2]	
   return val

#################################
#main program loop
#################################

while 1:
   try:
      time.sleep(0.05) #10 hz poll
      sound_sens = readADC(7)
      print "SND = ", sound_sens

      if (sound_sens < 100):
          print "SOUND!!"
          for i in range (8):
             ser.write(b'a') #turn left
             time.sleep(0.2) 
             ser.write(b'd') #turn right
             time.sleep(0.2)
          ser.write(b' ') #stop 

   except KeyboardInterrupt:
      break

print "\n\nByeByePyPiBot!\n"
