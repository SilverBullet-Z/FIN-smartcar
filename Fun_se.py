#coding=utf-8

import RPi.GPIO as GPIO
import time

servopin = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servopin, GPIO.OUT, initial=False)
p = GPIO.PWM(servopin,50) #50HZ
p.start(0)
time.sleep(2)

def turn(s,t):
  k=s
  if s<=t:
    while k<=t:
      p.ChangeDutyCycle(2.5 + 10 * k / 180)       #设置转动角度
      time.sleep(0.02)                            #等该20ms周期结束
      p.ChangeDutyCycle(0)                        #归零信号
      time.sleep(0.02)
      k+=10
    while k>=t:
      p.ChangeDutyCycle(2.5 + 10 * k / 180)       #设置转动角度
      time.sleep(0.02)                            #等该20ms周期结束
      p.ChangeDutyCycle(0)                        #归零信号
      time.sleep(0.02)
      k-=10
