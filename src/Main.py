from pyfirmata import Arduino, util
from src.ArduinoCom import BatterySensor, TempSensor
import time


board = Arduino('/dev/ttyUSB0')
batterySensor = BatterySensor(board, 'a:0:i')
tempSensor = TempSensor(board, 'a:1:i')

time.sleep(2)

print(batterySensor.getVoltage())
print(batterySensor.getChargeLevel())
print(batterySensor.isFullyCharged())
print(batterySensor.isDepleted())

board.exit()
