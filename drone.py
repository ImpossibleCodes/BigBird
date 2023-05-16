import board
import busio
import adafruit_bno055
import adafruit_pca9685

import read_sbus_from_GPIO
import time

"""
http://autoquad.org/wiki/wiki/configuring-autoquad-flightcontroller/frame-motor-mixing-table/#:~:text=together%20(practical%20examples)-,HEXA%20X,-OK%2C%20let%E2%80%99s%20take

ESC layout for hexacopter

    A-CW B-CCW
F-CCW        C-CW
    E-CW D-CCW

Transmitter channel layout for Taranis QX7
THR:            throttle
RUD/YAW: 2      rotate left/right
ELE/PITCH:      lean forward/backward
ROLL:           lean left/right



motor mix:
A: 1.0 * THR + 1.0 * PIT + 0.5 * ROL - 1.0 * YAW
B: 1.0 * THR + 1.0 * PIT - 0.5 * ROL + 1.0 * YAW
C: 1.0 * THR + 0.0 * PIT - 1.0 * ROL - 1.0 * YAW
D: 1.0 * THR - 1.0 * PIT - 0.5 * ROL + 1.0 * YAW
E: 1.0 * THR - 1.0 * PIT + 0.5 * ROL - 1.0 * YAW
F: 1.0 * THR + 0.0 * PIT + 1.0 * ROL + 1.0 * YAW

"""

def setup():
    SBUS_PIN = 4 #pin where sbus wire is plugged in

    reader = read_sbus_from_GPIO.SbusReader(SBUS_PIN)
    reader.begin_listen()

    i2c = busio.I2C(board.SCL, board.SDA)
    pca = adafruit_pca9685.PCA9685(i2c)
    imu = adafruit_bno055.BNO055_I2C(i2c)
    ESC1 = pca.channels[1]
    ESC2 = pca.channels[2]
    ESC3 = pca.channels[3]
    ESC4 = pca.channels[4]
    ESC5 = pca.channels[5]
    ESC6 = pca.channels[6]
    return reader, ESC1, ESC2, ESC3, ESC4, ESC5, ESC6

def motor_mix(throttle, pitch, roll, yaw):
    a = 1.0 * throttle + 1.0 * pitch + 0.5 * roll - 1.0 * yaw
    b = 1.0 * throttle + 1.0 * pitch - 0.5 * roll + 1.0 * yaw
    c = 1.0 * throttle + 0.0 * pitch - 1.0 * roll - 1.0 * yaw
    d = 1.0 * throttle - 1.0 * pitch - 0.5 * roll + 1.0 * yaw
    e = 1.0 * throttle - 1.0 * pitch + 0.5 * roll - 1.0 * yaw
    f = 1.0 * throttle + 0.0 * pitch + 1.0 * roll + 1.0 * yaw
    return a, b, c, d, e, f

def control_loop(throttle, yaw, pitch, roll, imu):
    ESC1.duty_cycle = 0xFFFF
    pass


reader, ESC1, ESC2, ESC3, ESC4, ESC5, ESC6 = setup()

#wait until connection is established
while(not reader.is_connected()):
    time.sleep(.2)

#Note that there will be nonsense data for the first 10ms or so of connection
#until the first packet comes in.
time.sleep(.1)

while True:
    try:
        is_connected = reader.is_connected()
        packet_age = reader.get_latest_packet_age() #milliseconds

        #returns list of length 16, so -1 from channel num to get index
        channel_data = reader.translate_latest_packet()
        
        #
        #Do something with data here!
        #ex:print(f'{channel_data[0]}')
        #

    except KeyboardInterrupt:
        #cleanup cleanly after ctrl-c
        reader.end_listen()
        exit()
    except:
        #cleanup cleanly after error
        reader.end_listen()
        raise



    

