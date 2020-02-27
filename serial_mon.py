#!/usr/bin/env pythonn
import sys
from threading import Thread
#from bme280 import process_bme_reading
from rflib import rf2serial, fetch_messages
import rflib
from time import sleep
import time

def inbound_message_processing():
  try:
    while (True):
        sleep(0.2)
        fetch_messages(0);
        while len(rflib.processing_queue)>0:
            message = rflib.processing_queue.pop(0)
            print (time.strftime("%c")+" "+message[0]+" "+message[1])
        if rflib.event.is_set():
            break
  except Exception as e: 
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print message
        print e
        rflib.event.set()
        exit()

def main():
  rflib.init()

  #start serial processing thread
  a=Thread(target=rf2serial, args=())
  a.start()
  
  #start response processing thread
  b=Thread(target=inbound_message_processing, args=())
  b.start()

  #Use this to inject some test messages
  #rflib.message_queue.insert(len(rflib.message_queue),("10", "AWAKE"))
  #rflib.message_queue.insert(len(rflib.message_queue),("10", "TMP20"))
  #rflib.message_queue.insert(len(rflib.message_queue),("10", "TMP21"))
  #rflib.message_queue.insert(len(rflib.message_queue),("10", "SLEEP"))

  while not rflib.event.is_set():
      try:
          sleep(1)
      except KeyboardInterrupt:
          rflib.event.set()
          break
  print rflib.event.is_set()
  
if __name__ == "__main__":
    try:
      main()
    except Exception as e: 
      template = "An exception of type {0} occurred. Arguments:\n{1!r}"
      message = template.format(type(e).__name__, e.args)
      print message
      print e
      rflib.event.set()
    finally:
      rflib.event.set()
      exit()
