#!/usr/bin/python3

import pytds
import RPi.GPIO as GPIO
import sys
from uuid import getnode
from mfrc522 import SimpleMFRC522
from time import sleep

# import from config.py
from config import server, database, username, password

reader = SimpleMFRC522()
debug = False

MAC = str(hex(getnode()))[2:]

GPIO.setup(40,GPIO.OUT) # LED on pin 40 / GPIO 21
GPIO.setup(36,GPIO.OUT) # Buzzer on pin 36 / GPIO 16

def debugMsg(message):
    ''' DebugMsg function to return debug messages '''
    if debug:
        print(message)

def getGPIOMode():
    ''' getGPIOMode function to display set GPIO mode '''
    if debug:
        mode = GPIO.getmode()
        if mode == 10:
            print("Mode = BOARD")
        elif mode == 11:
            print("Mode = BCM / GPIO")
        else:
            print("Mode is unset")

def alert(type):
    ''' Alert function to activate the LED and buzzer
    type parameter can be start-up, success or failure '''
    if type == "start-up":
        debugMsg("Buzzer ON")
        GPIO.output(36,GPIO.HIGH)
        sleep(0.0625)
        for i in range(5):
            debugMsg("Buzzer OFF")
            GPIO.output(36,GPIO.LOW)
            sleep(0.0625)
            debugMsg("Buzzer ON")
            GPIO.output(36,GPIO.HIGH)
            sleep(0.0625)
        debugMsg("Buzzer OFF")
        GPIO.output(36,GPIO.LOW)
    if type == "success":
        debugMsg("LED and buzzer ON")
        GPIO.output(40,GPIO.HIGH)
        GPIO.output(36,GPIO.HIGH)
        sleep(0.125)
        debugMsg("Buzzer OFF")
        GPIO.output(36,GPIO.LOW)
        sleep(1) # pause between scans
        GPIO.output(40,GPIO.LOW) # turn off LED
    if type == "failure":
        debugMsg("LED and buzzer ON")
        GPIO.output(40,GPIO.HIGH)
        GPIO.output(36,GPIO.HIGH)
        sleep(0.0625)
        for i in range(3):
            debugMsg("Buzzer OFF")
            GPIO.output(36,GPIO.LOW)
            sleep(0.0625)
            debugMsg("Buzzer ON")
            GPIO.output(36,GPIO.HIGH)
            sleep(0.0625)
        debugMsg("Buzzer OFF")
        GPIO.output(36,GPIO.LOW)
        sleep(1) # pause between scans
        GPIO.output(40,GPIO.LOW) # turn off LED

getGPIOMode() # display GPIO Mode if in debug

# play start-up alert
alert("start-up")

# Main program loop starts here
while True:
   try:
      uuid = reader.read_id()
      debugMsg(uuid)
      debugMsg("HEX = ")
      hexuuid = format(uuid,"010x")
      debugMsg(hexuuid)
      debugMsg("Reversed HEX = ")
      rehexuuid = "".join(map(str.__add__, hexuuid[-2::-2] ,hexuuid[-1::-2]))
      debugMsg(rehexuuid)
      debugMsg("Stripped reversed HEX = ")
      strrehexuuid = rehexuuid[-8:]
      debugMsg(strrehexuuid)
      debugMsg("Final dec version = ")
      cardDec = int(strrehexuuid, 16)
      debugMsg(cardDec)
      cardnum = str(cardDec)
      debugMsg("Device MAC = ")
      debugMsg(MAC)
      with pytds.connect(server, database, username, password) as conn:
          with conn.cursor() as cur:
              cur.execute("SELECT * FROM VwADSIUsers WHERE pager = '" + cardnum + "'")
              sqlResult = cur.fetchall()
              if cur.rowcount == 1: # we have 1 row returned
                  debugMsg(sqlResult[0])
                  if len(sqlResult[0]) == 6: # we have 6 items in the object
                      debugMsg("Inserting data now")
                      cur.execute("INSERT INTO TblScan (GUID, dteScanTime, cardnum, txtMACAddress) VALUES ('" + str(sqlResult[0][0]) + "', CURRENT_TIMESTAMP, '" + cardnum + "', '" + MAC + "')")
                      conn.commit()
                      alert("success")
                  else: # row did not have the correct number of items in it
                      curr.execute("INSERT INTO TblLogs (txtMessage, dteScanTime) VALUES ('SQL SELECT for card number " + cardnum + " did not return the expected number of columns', CURRENT_TIMESTAMP)")
                      conn.commit()
                      alert("failure")
              elif cur.rowcount > 1: # we have more than one row returned
                  cur.execute("INSERT INTO TblLogs (txtMessage, dteScanTime) VALUES ('More than one match found for card number " + cardnum + "', CURRENT_TIMESTAMP)")
                  conn.commit()
                  alert("failure")
              else: # No rows returned
                  debugMsg("Error - Card not known!")
                  debugMsg(cardnum)
                  cur.execute("INSERT INTO TblScan (cardnum, dteScanTime, txtMACAddress) VALUES ('" + cardnum + "', CURRENT_TIMESTAMP, '" + MAC + "')")
                  cur.execute("INSERT INTO TblLogs (txtMessage, dteScanTime) VALUES ('No match found for card number " + cardnum + "', CURRENT_TIMESTAMP)")
                  conn.commit()
                  alert("failure")
   except KeyboardInterrupt:
      GPIO.cleanup()
      sys.exit(1)
