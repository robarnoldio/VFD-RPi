#!/usr/bin/python
##################################################
# 20x2 IEE VFD test program and function library #
#                                                #
# Forked from the lcd_16x2.py script below       #
# 3/8/2016 Rob Arnold                            #
# robarnold.io                                   #
##################################################


#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#  lcd_16x2.py
#  16x2 LCD Test Script
#
# Author : Matt Hawkins
# Date   : 06/04/2015
#
# http://www.raspberrypi-spy.co.uk/
#
# Copyright 2015 Matt Hawkins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------



# The wiring for the VFD is three categories:

### POWER CONNECTIONS ###
# 6 : GND
# 2 : 5V


### CONTROL CONNECTIONS ###   
# 18: RS (Register Select)
# 17: R/W (Read Write)       - GROUND THIS PIN
# 20: Enable or Strobe

### DATA CONNECTIONS (8-bit parallel mode) ###
# 15: Data Bit 0             
# 13: Data Bit 1             
# 11: Data Bit 2             
# 9 : Data Bit 3             
# 7 : Data Bit 4
# 5 : Data Bit 5
# 3 : Data Bit 6
# 1 : Data Bit 7

#import
import RPi.GPIO as GPIO
import time

# Define GPIO to VFD mapping
# These are the BCM numbers of the GPIOs
# Not the pin numbers
VFD_RS = 7    #pin 26
VFD_E  = 8    #pin 24
VFD_D0 = 6    #pin 31
VFD_D1 = 13   #pin 33
VFD_D2 = 19   #pin 35
VFD_D3 = 26   #pin 37
VFD_D4 = 25   #pin 22
VFD_D5 = 24   #pin 18
VFD_D6 = 23   #pin 16
VFD_D7 = 18   #pin 12


# Define some device constants
VFD_WIDTH = 20    # Maximum characters per line
VFD_CHR = True
VFD_CMD = False

################### these are different than HD44780
VFD_LINE_1 = 0x80 # VFD RAM address for the 1st line
VFD_LINE_2 = 0x94 # VFD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def main():
  # Main program block
  
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(VFD_E, GPIO.OUT)  # E
  GPIO.setup(VFD_RS, GPIO.OUT) # RS
  GPIO.setup(VFD_D0, GPIO.OUT) # DB0
  GPIO.setup(VFD_D1, GPIO.OUT) # DB1
  GPIO.setup(VFD_D2, GPIO.OUT) # DB2
  GPIO.setup(VFD_D3, GPIO.OUT) # DB3
  GPIO.setup(VFD_D4, GPIO.OUT) # DB4
  GPIO.setup(VFD_D5, GPIO.OUT) # DB5
  GPIO.setup(VFD_D6, GPIO.OUT) # DB6
  GPIO.setup(VFD_D7, GPIO.OUT) # DB7


  # Initialise display
  vfd_init()

  while True:

    vfd_string("Rasbperry Pi",VFD_LINE_1)

    time.sleep(1) # 1 second delay

    vfd_string("20x2 VFD Test",VFD_LINE_2)

    time.sleep(1) # 1 second delay

    vfd_string("12345678901234567890",VFD_LINE_1)

    time.sleep(1) # 1 second delay

    vfd_string("abcdefghijklmnopqrst",VFD_LINE_2)

    time.sleep(1) # 1 second delay

    vfd_string("this is awesome",VFD_LINE_1)

    time.sleep(1) # 1 second delay

    vfd_string("you know it",VFD_LINE_2)

    time.sleep(1) # 1 second delay

    vfd_string("hardware hacking",VFD_LINE_1)

    time.sleep(1) # 1 second delay

    vfd_string("rob@robarnold.io",VFD_LINE_2)

    time.sleep(1) # 1 second delay


def vfd_init():
  # Initialise display
  vfd_byte(0x02,VFD_CMD) # 00001x home cursor
  vfd_byte(0x01,VFD_CMD) # 000001 Clear display

  time.sleep(E_DELAY)

def vfd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(VFD_RS, mode) # RS

  GPIO.output(VFD_D0, False)
  GPIO.output(VFD_D1, False)
  GPIO.output(VFD_D2, False)
  GPIO.output(VFD_D3, False)
  GPIO.output(VFD_D4, False)
  GPIO.output(VFD_D5, False)
  GPIO.output(VFD_D6, False)
  GPIO.output(VFD_D7, False)
  
  if bits&0x01==0x01:
    GPIO.output(VFD_D0, True)
  if bits&0x02==0x02:
    GPIO.output(VFD_D1, True)
  if bits&0x04==0x04:
    GPIO.output(VFD_D2, True)
  if bits&0x08==0x08:
    GPIO.output(VFD_D3, True)
  if bits&0x10==0x10:
    GPIO.output(VFD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(VFD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(VFD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(VFD_D7, True)

  # Toggle 'Enable' pin
  vfd_toggle_enable()

def vfd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(VFD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(VFD_E, False)
  time.sleep(E_DELAY)

def vfd_string(message,line):
  # Send string to display
  message = message.ljust(VFD_WIDTH," ")

  vfd_byte(line, VFD_CMD)

  for i in range(VFD_WIDTH):
    vfd_byte(ord(message[i]),VFD_CHR)

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    vfd_byte(0x01, VFD_CMD)
    vfd_string("Goodbye!",VFD_LINE_1)
    GPIO.cleanup()
