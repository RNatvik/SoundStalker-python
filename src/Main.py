from pyfirmata import Arduino, util
from .ArduinoCom import BatterySensor, TempSensor
from .PiSensors import SonicSensor
import RPi.GPIO as GPIO
import time


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    board = Arduino('/dev/ttyUSB0')
    batterySensor = BatterySensor(board, 'a:0:i')
    tempSensor = TempSensor(board, 'a:1:i')

    sonic = SonicSensor()

    time.sleep(2)

    print(batterySensor.getVoltage())
    print(batterySensor.getChargeLevel())
    print(batterySensor.isFullyCharged())
    print(batterySensor.isDepleted())

    board.exit()