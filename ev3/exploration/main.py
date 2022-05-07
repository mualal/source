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


def wait_and_display_clear(brick):
    wait(100)
    brick.screen.clear()


# Create your objects here.
ev3 = EV3Brick()
test_motor = Motor(Port.A)
test_eyes = InfraredSensor(Port.S1)
test_touch_sensor = TouchSensor(Port.S2)
test_gyro_sensor = GyroSensor(Port.S3)

# Write your program here.
ev3.speaker.beep()

while True:
    ev3.screen.draw_text(10, 60, 'Dist: ' + str(test_eyes.distance()) + ' cm')

    if test_eyes.distance() < 50:
        test_motor.run_target(500, 90)

    if test_touch_sensor.pressed():
        break

    wait_and_display_clear(ev3)

ev3.speaker.beep(frequency=1000, duration=500)

while True:
        
    ev3.screen.draw_text(10, 60, 'Gyro: ' + str(test_gyro_sensor.speed()))

    if test_touch_sensor.pressed():
        break

    wait_and_display_clear(ev3)
