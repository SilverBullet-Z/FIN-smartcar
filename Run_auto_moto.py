#coding=utf-8

'''
Run_auto_moto 自动程序

'''
import RPi.GPIO as gpio
import time

gpio.setwarnings(False)

#车轮控制类
class wheel:
	pins={'lt':[35,37],'rt':[33,31]}#车轮IO口 +\-
	#初始化
	def __init__(self,name):
		self.name=name
		self.pin=wheel.pins[self.name]
		gpio.setmode(gpio.BOARD)
		gpio.setup(self.pin[0],gpio.OUT)
		gpio.setup(self.pin[1],gpio.OUT)
		gpio.output(self.pin[0],0)
		gpio.output(self.pin[1],0)
		self.stop()
	def fowd(self):
		gpio.output(self.pin[0],gpio.HIGH)
		gpio.output(self.pin[1],gpio.LOW)
	def stop(self):
		gpio.output(self.pin[0],False)
		gpio.output(self.pin[1],False)
	def back(self):
		gpio.output(self.pin[0],gpio.LOW)
		gpio.output(self.pin[1],gpio.HIGH)
#小车执行类
class Car:
	wheels=[wheel('lt'),wheel('rt')]
	@staticmethod
	def init():
		gpio.setmode(gpio.BOARD)
		for wheel in Car.wheels: wheel.stop()
	@staticmethod
	def stop():
		for wheel in Car.wheels: wheel.stop()
	@staticmethod
	def fowd():
		Car.stop()
		for wheel in Car.wheels: wheel.fowd()
		time.sleep(0.5)  #直行时间
		Car.stop()
	@staticmethod
	def back():
		Car.stop()
		for wheel in Car.wheels: wheel.back()
		time.sleep(0.5)  #直行时间
		Car.stop()
	@staticmethod
	def left():
		Car.stop()
		Car.wheels[1].fowd()
		Car.wheels[0].back()
		time.sleep(0.3)  #左转时间
		Car.stop()
	@staticmethod
	def right():
		Car.stop()
		Car.wheels[0].fowd()
		Car.wheels[1].back()
		time.sleep(0.3)  #右转时间
		Car.stop()


