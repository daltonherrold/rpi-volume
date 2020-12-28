import RPi.GPIO as GPIO
from time import time, sleep 
from client import get_processes, increment, decrement
from draw import setup, draw_process 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

draw, disp, font, image = setup()

TOP = 17
BOTTOM = 22

index = 0
processes = []
refresh_time = time()

while True:
    if time() > refresh_time:
        refresh_time = time() + 5
        if len(processes) > 0:
            temp_name = processes[index]['name']
            processes = get_processes()
            for i in range(len(processes)):
                if processes[i]['name'] == temp_name:
                    index = i
                    break
        else:
            processes = get_processes()	
        if len(processes) > 0:
            draw_process(draw, disp, font, image, processes[index])
        else:
            draw_process(draw, disp, font, image, {'name': 'None', 'volume': 0})
    if GPIO.input(TOP) == GPIO.HIGH:
        other = False 
        for i in range(125):
            sleep(0.001)
            if GPIO.input(BOTTOM) == GPIO.HIGH:
                other = True 
        if other:
            index = (index + 1) % len(processes)
            if len(processes) > 0:
                draw_process(draw, disp, font, image, processes[index])
            else:
                draw_process(draw, disp, font, image, {'name': 'None', 'volume': 0})
        else:
            if len(processes) > 0:
                new_vol = increment(processes[index]['name'])
                processes[index]['volume'] = new_vol
                draw_process(draw, disp, font, image, processes[index])
            else:
                draw_process(draw, disp, font, image, {'name': 'None', 'volume': 0})
    if GPIO.input(BOTTOM) == GPIO.HIGH:
        other = False 
        for i in range(125):
            sleep(0.001)
            if GPIO.input(TOP) == GPIO.HIGH:
                other = True 
        if other:
            index = (index + 1) % len(processes)
            if len(processes) > 0:
                draw_process(draw, disp, font, image, processes[index])
            else:
                draw_process(draw, disp, font, image, {'name': 'None', 'volume': 0})
        else:
            if len(processes) > 0:
                new_vol = decrement(processes[index]['name'])
                processes[index]['volume'] = new_vol
                draw_process(draw, disp, font, image, processes[index])
            else:
                draw_process(draw, disp, font, image, {'name': 'None', 'volume': 0})
