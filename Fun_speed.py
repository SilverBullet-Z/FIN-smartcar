#coding=utf-8

import RPi.GPIO as GPIO
import time
import redis
#速度的计算公式应该为  （n/20）×(65×10-1×π)  即n*1.02101761
INTO = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(INTO, GPIO.IN)

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)

N=1.02101761
count = 0
print "0"
try:

	wd=r.get('status')
	
	while wd=='q':

		into = GPIO.input(INTO)
		print "1"
		if into==0:
			print "2"
			count+=count		
			#输出速度，每1s重置
			if 1000==count:
				print '3'
				vel =N*(count/20);
				sp=vel+'cm/s(R)'
				r.set('speed',sp)
				count = 0	

except Exception, e:
	print "Sorry for the error, I have to suspend this service for you"
	r.set('print','wrong')

