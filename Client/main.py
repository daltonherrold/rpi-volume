import RPi.GPIO as GPIO
from time import sleep 
from client import get_processes, increment, decrement
from draw import setup, draw_process 
import threading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

draw, disp, font, image = setup()

TOP = 17
BOTTOM = 22

index = 0
processes = []

def draw_screen():
    if len(processes) > 0:
        draw_process(draw, disp, font, image, processes[index], '{}/{}'.format(index+1, len(processes)))
    else:
        draw_process(draw, disp, font, image, {'name': 'None', 'volume': 0}, '0/0')


class refreshProcesses (threading.Thread):
   def __init__(self, threadID):
      threading.Thread.__init__(self)
      self.threadID = threadID
   def run(self):
       global processes
       global lock
       global index
       while True:
            if len(processes) > 0:
                lock.acquire()
                temp_name = processes[index]['name']
                processes = get_processes()
                for i in range(len(processes)):
                    if processes[i]['name'] == temp_name:
                        index = i
                        break
            else:
                temp = get_processes()	
                lock.acquire()
                processes = temp
            draw_screen()
            lock.release()
            sleep(5)

lock = threading.Lock()

thread = refreshProcesses("Processing-Thread")
thread.start()

while True:
    if GPIO.input(TOP) == GPIO.HIGH:
        other = False 
        for i in range(125):
            sleep(0.001)
            if GPIO.input(BOTTOM) == GPIO.HIGH:
                other = True 
        lock.acquire()
        if other:
            index = (index + 1) % len(processes)
            draw_screen()
        else:
            if len(processes) > 0:
                new_vol = increment(processes[index]['name'])
                processes[index]['volume'] = new_vol
            draw_screen()
        lock.release()
    if GPIO.input(BOTTOM) == GPIO.HIGH:
        other = False 
        for i in range(125):
            sleep(0.001)
            if GPIO.input(TOP) == GPIO.HIGH:
                other = True 
        lock.acquire()
        if other:
            index = (index + 1) % len(processes)
            draw_screen()
        else:
            if len(processes) > 0:
                new_vol = decrement(processes[index]['name'])
                processes[index]['volume'] = new_vol
            draw_screen()
        lock.release()

