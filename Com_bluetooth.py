#-*- coding:utf-8 -*-
import bluetooth
import threading

import redis
import time

import Run_mt_moto

#服务器套接字(用来接收新链接)
server_socket=None

r=redis.Redis(host='127.0.0.1',port=6379)
#连接套接字服务子线程
def serveSocket(sock,info):
    #开个死循环等待客户端发送信息
    while True:
        #接收1024个字节,然后以UTF-8解码(中文),如果没有可以接收的信息则自动阻塞线程(API)
        receive=sock.recv(1024).decode('utf-8');
        #打印刚刚读到的东西(info=地址)
        print('['+str(info)+']'+receive);
        r.set('status',receive)
        pt=r.get('print')+"\n"
        sock.send(pt)
        sock.send('speed')
        if  r.get('status')== 'w':
            Run_mt_moto.Car.fowd()
            sock.send('forward...')
        if  r.get('status')== 'a':
            Run_mt_moto.Car.left()
            sock.send('left...')
        if  r.get('status')== 's':
            Run_mt_moto.Car.back()
            sock.send('back...')
        if  r.get('status')== 'd':
            Run_mt_moto.Car.right()
            sock.send('right...')
        if  r.get('status')== 'p':
            Run_mt_moto.Car.stop()
            sock.send('stop...')

        #为了返回好看点,加个换行
        #receive=receive+"\n";
        #回传数据给发送者
        #sock.send(receive.encode('utf-8'));
 
#主线程
 
#创建一个服务器套接字,用来监听端口
server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM);
#允许任何地址的主机连接,未知参数:1(端口号,通道号)
server_socket.bind(("",1))
#监听端口/通道
server_socket.listen(1);
 
#开死循环 等待客户端连接
#本处应放在另外的子线程中
while True:
    #等待有人来连接,如果没人来,就阻塞线程等待(这本来要搞个会话池,以方便给不同的设备发送数据)
    sock,info=server_socket.accept();
    #打印有人来了的消息
    print(str(info[0])+' Connected!');
    #创建一个线程专门服务新来的连接(这本来应该搞个线程池来管理线程的)
    t=threading.Thread(target=serveSocket,args=(sock,info[0]))
    #设置线程守护,防止程序在线程结束前结束
    t.setDaemon(True)
    #启动线程
    t.start();