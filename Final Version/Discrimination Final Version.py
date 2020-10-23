# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 12:13:36 2019

@author: Nelson
"""

import RPi.GPIO as GPIO
import time
import numpy as np
#import pandas as pd
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
t_start = [] #Time for Trial Start
t_response = [] #Response Time
t_result = []
t_side = []# Correct Side
# In[ ]:

##def Export_Data(t_start, t_response, t_result, t_side):
##    data_array = np.matrix(t_start, t_response, t_result)#, t_side)
##    tran_data = data_array.getT()
##    print(tran_data)
##    np.savetxt("Trial Results.csv",data_array, delimiter=",")

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
    #print(time.asctime())

def color_select(color):
    if(color == 1):
        GPIO.setup(led_1_red, GPIO.OUT)
        GPIO.setup(led_2_red, GPIO.OUT)
        return[led_1_red, led_2_red]
    elif(color == 2):
        GPIO.setup(led_1_green, GPIO.OUT)
        GPIO.setup(led_2_green, GPIO.OUT)
        return[led_1_green, led_2_green]
    elif(color == 3):
        GPIO.setup(led_1_blue, GPIO.OUT)
        GPIO.setup(led_2_blue, GPIO.OUT)
        return[led_1_blue,led_2_blue]

def R_or_L(side):
    if(side == 1):
        return "Left"
    elif(side == 2):
        return "Right"

def All_Out(color_array):
    GPIO.output(int(color_array[0]), False)
    GPIO.output(int(color_array[1]), False)
    GPIO.output(int(color_array[2]), False)
    GPIO.output(int(color_array[3]), False)
    
# In[10]:
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_UP)#Button
GPIO.setup(buzzer_motor, GPIO.OUT)
GPIO.setup(IR_sensor_1, GPIO.IN)
GPIO.setup(IR_sensor_2, GPIO.IN)
a=0
max_tia = int(input("How many times do you want to reinforce the fish? "))
curside = Trial_Sides(max_tia)
color_side = Trial_Sides(max_tia)

color_correct= int(input("Choose a correct color: 1 = red, 2 = green, 3 = blue: "))
color_wrong = int(input("Choose a wrong color: 1 = red, 2 = green, 3 = blue: "))
if(color_correct == color_wrong):
    while(color_correct == color_wrong):
        print("ERROR: both the right and wrong color are the same" )
        color_correct= int(input("Choose a correct color: 1 = red, 2 = green, 3 = blue: "))
        color_wrong = int(input("Choose a wrong color: 1 = red, 2 = green, 3 = blue: "))
rc = color_select(color_correct)
wc = color_select(color_wrong)
color_array = np.concatenate((rc,wc), axis=None)
print(color_array)
All_Out(color_array)

try:
    for x in range(max_tia):
        light_side = curside[x]
        strside = R_or_L(light_side)
        t_side.append(strside)
        strside = str(strside) + "side"
        b = 0
        t_start.append(time.asctime())
        if(light_side == 1):
            GPIO.output(int(color_array[0]), True)
            GPIO.output(int(color_array[3]), True)
            while(b == 0):
                if(GPIO.input(button) == False):
                    t_response.append(time.asctime())
                    feeder()
                    b = 1
                    print("button pressed")
                    t_result.append("Override")
                elif(GPIO.input(IR_sensor_1) == False):
                    t_response.append(time.asctime())
                    feeder()
                    b = 1
                    t_result.append("Success")
                elif(GPIO.input(IR_sensor_2) == False):
                    t_response.append(time.asctime())
                    print("Wrong Responce, Trial paused for 5 seconds")
                    GPIO.output(int(color_array[0]), False)
                    GPIO.output(int(color_array[3]), False)
                    t_result.append("Failure")
                    time.sleep(5)
                    #time.sleep(60)
                    b = 1  
            GPIO.output(int(color_array[0]), False)
            GPIO.output(int(color_array[3]), False)
        elif(light_side == 2):
            GPIO.output(int(color_array[1]), True)
            GPIO.output(int(color_array[2]), True)
            while(b == 0):
                if(GPIO.input(button) == False):
                    t_response.append(time.asctime())
                    feeder()
                    b = 1
                    print("button pressed, Manual Override")
                    t_result.append("Override")
                elif(GPIO.input(IR_sensor_2)== False):
                    t_response.append(time.asctime())
                    feeder()
                    b = 1
                    t_result.append("Success")
                elif(GPIO.input(IR_sensor_1)== False):
                    t_response.append(time.asctime())
                    print("Wrong Responce, Trial paused for 5 seconds")
                    GPIO.output(int(color_array[1]), False)
                    GPIO.output(int(color_array[2]), False)
                    t_result.append("Failure")
                    time.sleep(5)
                    #time.sleep(60)
                    b = 1               
            GPIO.output(int(color_array[1]), False)
            GPIO.output(int(color_array[2]), False)
        time.sleep(5)
    print("Max Trials Reached---ending program")
##    Export_Data(t_start, t_response, t_result, t_side)
    GPIO.cleanup()
    
except(KeyboardInterrupt):
    print("program manually terminated")
    Export_Data(t_start, t_response, t_result, t_side)
    GPIO.cleanup()

except:
    Export_Data(t_start, t_response, t_result, t_side)
    GPIO.cleanup()

