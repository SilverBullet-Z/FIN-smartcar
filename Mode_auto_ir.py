#coding=utf-8

'''
Mode_auto_ir.py 智能小车红外避障主模块
'''

import RPi.GPIO as GPIO

import sys
import time
import redis

import Run_auto_moto
#import Run_pwm_moto 

#主程序


LL = 21
LR = 22
RL = 23
RR = 24

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LL,GPIO.IN)
GPIO.setup(LR,GPIO.IN)
GPIO.setup(RL,GPIO.IN)
GPIO.setup(RR,GPIO.IN)

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)

try:
        while True:

                wd =r.get('status')

                if wd == 'io' :

                        print "Now Mode_auto_ir is waitting "
                        time.sleep(1)                        
                        #GPIO.cleanup()
                        r.set('print','running')
                        #breakyou exit the Auto_ir MODE and
                
                elif wd == 'er':
                        print "Now you exit the Auto_ir MODE "
                        GPIO.cleanup()
                        sys.exit(0)

                elif wd == 'ir':

                        print "Now the Auto_ir MODE is running"
                        r.set('print','exit')

                        BLL = GPIO.input(LL)
                        BLR = GPIO.input(LR)
                        BRL = GPIO.input(RL)
                        BRR = GPIO.input(RR)

                        if BLL == True and BLR == True and BRL == True and BRR == True:
                                Run_auto_moto.Car.back()
                                print "1"
                                
                        elif BLL == False and BLR == True and BRL == True and BRR == True:
                                Run_auto_moto.Car.right()
                                print "2"
                                
                        elif BLL == True and BLR == False and BRL == True and BRR == True:
                                Run_auto_moto.Car.right()
                                print "3"
                                               
                        elif BLL == True and BLR == True and BRL == False and BRR == True:
                                Run_auto_moto.Car.left()
                                print "4"
                                
                        elif BLL == True and BLR == True and BRL == True and BRR == False:
                                Run_auto_moto.Car.left()
                                print "5"
                                
                        elif BLL == False and BLR == False and BRL == True and BRR == True:
                                Run_auto_moto.Car.right()
                                print "6"
                                
                        elif BLL == False and BLR == True and BRL == False and BRR == True:
                                Run_auto_moto.Car.fowd()
                                time.sleep(0.4)
                                Run_auto_moto.Car.left()
                                time.sleep(0.3)
                                print "7"
                                                           
                        elif BLL == False and BLR == True and BRL == True and BRR == False:
                                Run_auto_moto.Car.back()
                                print "8"
                                
                        elif BLL == True and BLR == False and BRL == False and BRR == True:
                                Run_auto_moto.Car.fowd()
                                time.sleep(0.4)
                                Run_auto_moto.Car.left()
                                time.sleep(0.3)
                                print "9"
                                                       
                        elif BLL == True and BLR == False and BRL == True and BRR == False:
                                Run_auto_moto.Car.fowd()
                                time.sleep(0.4)
                                Run_auto_moto.Car.left()
                                time.sleep(0.3)
                                print "10"
                                                        
                        elif BLL == True and BLR == True and BRL == False and BRR == False:
                                Run_auto_moto.Car.left()
                                print "11"
                                                     
                        elif BLL == False and BLR == False and BRL == False and BRR == True:
                                Run_auto_moto.Car.fowd()
                                time.sleep(0.4)
                                Run_auto_moto.Car.right()
                                time.sleep(0.3)
                                print "12"
                                                        
                        elif BLL == False and BLR == False and BRL == True and BRR == False:
                                Run_auto_moto.Car.fowd()
                                time.sleep(0.4)
                                Run_auto_moto.Car.right()
                                time.sleep(0.3)
                                print "13"
                                
                        elif BLL == False and BLR == True and BRL == False and BRR == False:
                                Run_auto_moto.Car.fowd()
                                time.sleep(0.4)
                                Run_auto_moto.Car.left()
                                time.sleep(0.3)
                                print "14"
                                
                        elif BLL == True and BLR == False and BRL == False and BRR == False:
                                Run_auto_moto.Car.fowd()
                                time.sleep(0.4)
                                Run_auto_moto.Car.left()
                                time.sleep(0.3)
                                print "15"
                                
                        elif BLL == False and BLR == False and BRL == False and BRR == False:
                                Run_auto_moto.Car.fowd()
                                time.sleep(0.4)
                                Run_auto_moto.Car.right()
                                time.sleep(0.3)
                                print "16"
                        time.sleep(0.4)
        raw_input()
                                                                      
except Exception, e:
        print "Sorry for the error, I have to suspend this service for you"
        r.set('print','wrong')
        GPIO.cleanup()

