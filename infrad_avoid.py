#!/usr/bin/python
# coding=utf-8
# 本段代码实现树莓派智能小车的红外避障效果
# 代码使用的树莓派GPIO是用的BCM编码方式。
"""
* @par Copyright (C): 2010-2020, hunan CLB Tech
* @file         infrad_avoid
* @version      V2.0
* @details
* @par History

@author: zhulin
"""
from LOBOROBOT import LOBOROBOT  # 载入机器人库
import RPi.GPIO as GPIO
import time
import sys

SensorRight = 16  # 右侧红外避障传感器
SensorLeft = 12  # 左侧红外避障传感器

BtnPin = 19  # 按键端口
Gpin = 5  # 绿色LED灯接口
Rpin = 6  # 红色LED灯接口


# 按键控制函数
def keysacn():
    val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == False:
        val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == True:
        time.sleep(0.01)
        val = GPIO.input(BtnPin)
        if val == True:
            GPIO.output(Rpin, 1)
            while GPIO.input(BtnPin) == False:
                GPIO.output(Rpin, 0)
        else:
            GPIO.output(Rpin, 0)


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # 按物理位置给GPIOs编号
    GPIO.setup(Gpin, GPIO.OUT)  # 设置绿色Led引脚模式输出
    GPIO.setup(Rpin, GPIO.OUT)  # 设置红色Led引脚模式输出
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 设置输入BtnPin模式，拉高至高电平(3.3V)
    GPIO.setup(SensorRight, GPIO.IN)
    GPIO.setup(SensorLeft, GPIO.IN)


#if __name__ == '__main__':
#    setup()
#    clbrobot = LOBOROBOT()  # 实例化机器人对象
#    keysacn()  # 键盘控制函数#
#
#    try:
#        while True:
#            SR_2 = GPIO.input(SensorRight)
#            SL_2 = GPIO.input(SensorLeft)
#            if SL_2 == True and SR_2 == True:
#                print("t_up")
#                clbrobot.t_up(50, 0)
#            elif SL_2 == True and SR_2 == False:
#                print("Left")
#                clbrobot.turnLeft(50, 0)
#            elif SL_2 == False and SR_2 == True:
#                print("Right")
#                clbrobot.turnRight(50, 0)
#            else:
#                clbrobot.t_stop(0.3)
#                clbrobot.t_down(50, 0.4)
#                clbrobot.turnLeft(50, 0.5)
#    except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行子程序destroy()。
#        clbrobot.t_stop(0)
#        GPIO.cleanup()
