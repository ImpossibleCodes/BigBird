import board
import busio
import adafruit_pca9685
import time

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

ESC1 = pca.channels[1]
# ESC2 = pca.channels[2]
# ESC3 = pca.channels[3]
# ESC4 = pca.channels[4]
# ESC5 = pca.channels[5]
# ESC6 = pca.channels[6]

# arm esc
ESC1.duty_cycle = 0
print("arm esc 0")
time.sleep(0.5)
ESC1.duty_cycle = 0x7FFF
print("arm esc 1")
time.sleep(0.5)
ESC1.duty_cycle = 0
print("arm esc 2")


