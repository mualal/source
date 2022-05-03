#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
test_motor = Motor(Port.A)
test_eyes = UltrasonicSensor(Port.B)
test_touch_sensor = TouchSensor(Port.C)
test_gyro_sensor = GyroSensor(Port.D)


# Write your program here.
ev3.speaker.beep()

while True:

    print(test_eyes.distance())

    if test_eyes.distance() < 500:
        test_motor.run_target(500, 90)

    if test_touch_sensor.pressed():
        break

    wait(100)

ev3.speaker.beep(frequency=1000, duration=500)

while True:
    
    print(test_gyro_sensor.speed())

    wait(100)
