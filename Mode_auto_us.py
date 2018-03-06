#coding=utf-8

#Mode_auto_us.py 智能小车主程序
import time
import redis
import sys
import Run_auto_moto
import RPi.GPIO as gpio
import Fun_us
import Fun_se

#全局设定
max=320#地图大小
MP=[[0 for X in range(max)] for y in range(max)]#地图初始化
DIR=1#初始方向置1
JD=13#超声波判断障碍距离
XX=0; YY=0

class pin:#超声波IO
  ip=36  #Echo
  op=32   #Trig


class Auto:
  @staticmethod
  #行驶算法
  def Map(x,y):
    global MP,DIR
    global JD

    #Direction  根据方向获取坐标
    if DIR==1:
      fx=x; fy=y-1
      lx=x-1; ly=y
      rx=x+1; ry=y
    if DIR==2:
      fx=x+1; fy=y
      lx=x; ly=y-1
      rx=x; ry=y+1
    if DIR==3:
      fx=x; fy=y+1
      lx=x+1; ly=y
      rx=x-1; ry=y
    if DIR==4:
      fx=x-1; fy=y
      lx=x; ly=y+1
      rx=x; ry=y-1

    #超声波测距
    s=Fun_us.shot(pin.op,pin.ip)
    if s<JD: MP[fx][fy]=2
    if MP[fx][fy]==0: return 2
    else:
      Fun_se.turn(0,90)
      s=Fun_us.shot(pin.op,pin.ip)
      Fun_se.turn(90,180)
      if s<JD: MP[rx][ry]=2
      if MP[rx][ry]==0: return 1

      Fun_se.turn(180,90)
      s=Fun_us.shot(pin.op,pin.ip)
      Fun_se.turn(90,0)
      if s<JD: MP[lx][ly]=2
      if MP[lx][ly]==0: return 1
      if MP[fx][fy]==1: return 1
      if MP[rx][ry]==1: return 2
      if MP[lx][ly]==1: return 2
      return 1

  #方向变更
  @staticmethod
  def cd(cds):
    global DIR
    if cds==1: DIR+=1
    if cds==2: DIR-=1
    if DIR>4: DIR=4
    if DIR<1: DIR=1
    return dir
  #地图输出

  @staticmethod
  def mapout(kx):
    for i in range(kx):
      s=""
      for j in range(kx):
        s+=str(MP[160-kx2+j][160-kx2+i])
      print s

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)


#主程序
try:

  while True:

    wd =r.get('status')
    
    if wd=='es':
      print "Now you exit the Auto_us MODE "
      r.set('print','exit')
      gpio.cleanup()
      sys.exit(0)
    elif wd=='uo':
      print "Now Mode_auto_us is waitting "
      time.sleep(1)
      r.set('print','running')
    elif wd=='us':
      print "Now the Auto_ir MODE is running"
      r.set('print','pause')

      global JD
      global MODE
      Run_auto_moto.Car.stop()#暂定

      x=max//2; y=max//2
      MP[x][y]=1#脚底置11
      #kx=1#步数统计
      d=Auto.Map(x,y)#算法
      if d==1:
        #kx+=1
        Run_auto_moto.Car.back()
        #坐标变更
        if DIR==1: y-=1
        if DIR==2: x+=1
        if DIR==3: y+=1
        if DIR==4: x-=1
      elif d==2:
        Run_auto_moto.Car.right()
        Auto.cd(1)
      elif d==3:
        Run_auto_moto.Car.left()
        Auto.cd(2)
      MP[x][y]=1#脚底置11
      print "Run mode:",d,"  Direction:",DIR
      #Auto.mapout(10)
      time.sleep(0.2)#每个动作延时
  raw_input()
except Exception, e:

  print "Sorry for the error, I have to suspend this service for you"
  r.set('print','wrong')
  gpio.cleanup()
