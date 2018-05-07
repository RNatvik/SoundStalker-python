from src.ArduinoCom import BatterySensor, TempSensor


batterySensor = BatterySensor('/dev/ttyUSB0')
tempSensor = TempSensor('/dev/ttyUSB0')

print(batterySensor.getVoltage())
