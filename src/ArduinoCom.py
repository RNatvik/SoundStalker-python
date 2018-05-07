from pyfirmata import Arduino, util
import time


class BatterySensor:

    def __init__(self, arduino, pin):
        self.MAX_VOLTAGE = 4.2
        self.MIN_VOLTAGE = 3.0
        board = arduino
        self.iterator = util.Iterator(board)
        self.iterator.setDaemon(True)
        self.iterator.start()
        self.pin = board.get_pin(pin)

    def getVoltage(self):
        value = self.pin.read()
        return value * 5

    def getChargeLevel(self):
        currentVoltage = self.getVoltage()
        scale = self.MAX_VOLTAGE - self.MIN_VOLTAGE
        chargeLevel = ((currentVoltage - self.MIN_VOLTAGE) / scale) * 100
        return chargeLevel

    def isFullyCharged(self):
        batteryFull = False

        if self.getVoltage() > self.MAX_VOLTAGE:
            batteryFull = True

        return batteryFull

    def isDepleted(self):
        batteryDepleted = False

        if self.getVoltage() < self.MIN_VOLTAGE:
            batteryDepleted = True

        return batteryDepleted


class TempSensor:

    def __init__(self, arduino, pin):
        self.MAX_TEMP = 40
        board = arduino
        self.iterator = util.Iterator(board)
        self.iterator.setDaemon(True)
        self.iterator.start()
        self.pin = board.get_pin(pin)

    def getVoltage(self):
        value = self.pin.read()
        return value * 5000

    def getTemperature(self):
        voltage = self.getVoltage()
        temp = (voltage - 500) * 0.1
        return temp

    def isAboveThreshold(self):
        aboveThreshold = False

        if self.getTemperature() > self.MAX_TEMP:
            aboveThreshold = True

        return aboveThreshold


if __name__ == '__main__':
    try:
        board = Arduino('/dev/ttyUSB0')
        batterySensor = BatterySensor(board, 'a:0:i')
        tempSensor = TempSensor(board, 'a:1:i')
        print("Sleeping")
        time.sleep(2)
        print("Awake")

        while True:
            print("Battery sensor:\n" +
                  "Voltage (V): " + batterySensor.getVoltage() + "\n" +
                  "Charge level (%): " + batterySensor.getChargeLevel() + "\n" +
                  "Fully charged: " + str(batterySensor.isFullyCharged()) + "\n" +
                  "Depleted: " + str(batterySensor.isDepleted()) + "\n")

            print("Temperature Sensor:\n" +
                  "Voltage (mV): " + tempSensor.getVoltage() + "\n" +
                  "Temperature (C): " + tempSensor.getTemperature() + "\n" +
                  "Above Threshold: " + str(tempSensor.isAboveThreshold()) + "\n")

            time.sleep(0.5)
    finally:
        print("shutting down")
        board.exit()