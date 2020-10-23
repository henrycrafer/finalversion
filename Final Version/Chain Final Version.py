# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 12:13:36 2019

@author: Nelson
"""

import RPi.GPIO as GPIO
import time
import numpy as np
import pandas as pd
import random

#GPIO Pins Setup
setup_time = time.strftime("%d %b %y")
fish = str(input("What is the fish number? "))
led_1_red = 17
led_1_green = 27
led_1_blue = 22
led_2_red = 5
led_2_green = 6
led_2_blue = 13
led_yellow = 25
IR_sensor_1 = 23
IR_sensor_2 = 24
IR_sensor_3 = 26
buzzer_motor =12
button = 16
t_standard = [] 
t_f_start = []
t_r_start = []
t_response = [] 
t_result = []
t_side = []
# In[ ]:

def output(filename,t_number,t_standard, t_f_start,t_r_start, t_response, t_result, t_side):
    f_react = []
    c_react = []
    for x in range(len(t_number)):
         f = round(t_r_start[x]- t_f_start[x],3)
         c = round(t_response[x] -t_r_start[x],3)
         f_react.append(f)
         c_react.append(c)
    set_data=pd.DataFrame(
        {
            "Trial #": t_number,
            "Time Flash On": t_standard,
            "Time Flash Response": f_react,
            "Side Color Response": t_result,
            "Time Color Response": c_react,
            "Side Correct": t_side,
        })
    set_data = set_data[["Trial #","Time Flash On","Time Flash Response","Time Color Response","Side Correct","Side Color Response"]]
    set_data.head()
    print(set_data)
    path = "/home/pi/Downloads/" + filename + ".csv"
    set_data.to_csv(path)


def Trial_Sides(max_trials):
    sid = []
    past = [3, 3, 3]
    max = int(max_trials)+1
    for trial in range(1, max):
        r = random.randint(1, 2)
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
    return

def feeder():
    GPIO.output(buzzer_motor, True)
    time.sleep(.1)
    GPIO.output(buzzer_motor, False)

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
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(buzzer_motor, GPIO.OUT)
GPIO.setup(led_yellow, GPIO.OUT)
GPIO.setup(IR_sensor_1, GPIO.IN)
GPIO.setup(IR_sensor_2, GPIO.IN)
GPIO.setup(IR_sensor_3, GPIO.IN)
a=0
max_tia = int(input("How many times do you want to reinforce the fish? "))
t_number = np.arange(1,max_tia+1)
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
All_Out(color_array)

filename = fish + " " + str(color_correct) + "R-" + str(color_wrong) +"W (" + setup_time + ")" 

try:
    for x in range(max_tia):
        light_side = curside[x]
        strside = R_or_L(light_side)
        t_side.append(strside)
        strside = str(strside) + "side"
        b = 0
        set = 0
        t_standard.append(time.asctime())
        GPIO.output(led_yellow, True)
        t_f_start.append(time.time())
        while(set == 0):
                if(GPIO.input(IR_sensor_3) == False):
                    GPIO.output(led_yellow, False)
                    set = 1
        t_r_start.append(time.time())
        if(light_side == 1):
            GPIO.output(int(color_array[0]), True)
            GPIO.output(int(color_array[3]), True)
            while(b == 0):
                if(GPIO.input(button) == False):
                    t_response.append(time.time())
                    feeder()
                    b = 1
                    print("button pressed")
                    t_result.append("Override")
                elif(GPIO.input(IR_sensor_1) == False):
                    t_response.append(time.time())
                    feeder()
                    b = 1
                    t_result.append("Success")
                elif(GPIO.input(IR_sensor_2) == False):
                    t_response.append(time.time())
                    print("Wrong Responce, Trial paused for 5 seconds")
                    GPIO.output(int(color_array[0]), False)
                    GPIO.output(int(color_array[3]), False)
                    t_result.append("Failure")
                    time.sleep(5)
                    b = 1  
            GPIO.output(int(color_array[0]), False)
            GPIO.output(int(color_array[3]), False)
        elif(light_side == 2):
            GPIO.output(int(color_array[1]), True)
            GPIO.output(int(color_array[2]), True)
            while(b == 0):
                if(GPIO.input(button) == False):
                    t_response.append(time.time())
                    feeder()
                    b = 1
                    print("button pressed, Manual Override")
                    t_result.append("Override")
                elif(GPIO.input(IR_sensor_2)== False):
                    t_response.append(time.time())
                    feeder()
                    b = 1
                    t_result.append("Success")
                elif(GPIO.input(IR_sensor_1)== False):
                    t_response.append(time.time())
                    print("Wrong Responce, Trial paused for 5 seconds")
                    GPIO.output(int(color_array[1]), False)
                    GPIO.output(int(color_array[2]), False)
                    t_result.append("Failure")
                    time.sleep(5)
                    b = 1               
            GPIO.output(int(color_array[1]), False)
            GPIO.output(int(color_array[2]), False)
        time.sleep(1)
    print("Max Trials Reached---ending program")
    output(filename,t_number,t_standard, t_f_start,t_r_start, t_response, t_result, t_side)
    GPIO.cleanup()
    
except(KeyboardInterrupt):
    print("program manually terminated")
    GPIO.cleanup()
    output(filename,t_number,t_standard, t_f_start,t_r_start, t_response, t_result, t_side)
    
except:
    GPIO.cleanup()
    output(filename,t_number,t_standard, t_f_start,t_r_start, t_response, t_result, t_side)
    

