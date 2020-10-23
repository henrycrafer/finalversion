# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 12:13:36 2019

@author: pick
"""

import RPi.GPIO as GPIO
import time
import numpy as np
import random

#GPIO Pins Setup
led_1_red = 17
led_1_green = 27
led_1_blue = 22
led_2_red = 5
led_2_green = 6
led_2_blue = 13
led_yellow = 26
IR_sensor_1 = 23
IR_sensor_2 = 24
buzzer_motor =12
button = 16

# In[ ]:

def Trial_Sides(max_trials):
    sid = []
    past = [3, 3, 3]
    max = int(max_trials)+1
    for trial in range(1, max):
        #print("Trial " + str(trial))
        r = random.randint(1, 2)
        #print("                rnd draw = " + str(r))
        #print(past)
        if past[0] == past[1] == past[2] == 1:
            r = 2
            Update_list(r,past)
        elif past[0] == past[1] == past[2] == 2:
            r = 1
            Update_list(r,past)
        else:
            Update_list(r,past)
            r = past[2]
        sid.append(r)        
    return sid
    
def Update_list(r,past):
    past[0] = past[1]
    past[1] = past[2]
    past[2] = r
    #print(past)
    return


def feeder():
    GPIO.output(buzzer_motor, True)
    time.sleep(.2)
    GPIO.output(buzzer_motor, False)
    print(time.asctime())


# In[10]:
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_UP)#Button
GPIO.setup(buzzer_motor, GPIO.OUT)
GPIO.setup(IR_sensor_1, GPIO.IN)
GPIO.setup(IR_sensor_2, GPIO.IN)
a=0
max_tia = int(input("How many times do you want to reinforce the fish? "))
curside = Trial_Sides(max_tia)

color = int(input("Choose a color: 1 = red, 2 = green, 3 = blue: "))
if(color == 1):
    led_1 = led_1_red
    led_2 = led_2_red
    GPIO.setup(led_1, GPIO.OUT)
    GPIO.setup(led_2, GPIO.OUT)
elif(color == 2):
    led_1 = led_1_green
    led_2 = led_2_green
    GPIO.setup(led_1, GPIO.OUT)
    GPIO.setup(led_2, GPIO.OUT)
elif(color == 3):
    led_1 = led_1_blue
    led_2 = led_2_blue
    GPIO.setup(led_1, GPIO.OUT)
    GPIO.setup(led_2, GPIO.OUT)
               
try:
    GPIO.output(led_1, False)
    GPIO.output(led_2, False)
    for x in range(max_tia):
        light_side = curside[x]
        strside = str(light_side) + ","
        print(strside, "Press Button")
        b = 0
        
        if(light_side == 1):
            GPIO.output(led_1, True)
            while(b == 0):
                if(GPIO.input(button) == False):
                    feeder()
                    b = 1
                    print("button pressed")
                    #GPIO.output(led_1, False)
                elif(GPIO.input(IR_sensor_1) == False):
                    feeder()
                    b = 1
            GPIO.output(led_1, False)
        elif(light_side == 2):
            GPIO.output(led_2, True)
            while(b == 0):
                if(GPIO.input(button) == False):
                    feeder()
                    b = 1
                    print("button pressed")
                    #GPIO.output(led_1, False)
                elif(GPIO.input(IR_sensor_2) == False):
                    feeder()
                    b = 1
            GPIO.output(led_2, False)
        time.sleep(5)
    GPIO.cleanup()

except(KeyboardInterrupt):
    GPIO.cleanup()
    
    
