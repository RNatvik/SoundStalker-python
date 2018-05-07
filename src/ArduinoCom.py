from pyfirmata import Arduino


class BatterySensor:

    def __init__(self, USB_PORT):
        self.MAX_VOLTAGE = 4.2
        self.MIN_VOLTAGE = 3.0
        board = Arduino(USB_PORT)
        self.pin = board.get_pin('a:0:i')

    def getVoltage(self):
        value = self.pin.read()
        return value * 5

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

    def __init__(self, USB_PORT):
        self.MAX_TEMP = 40
        board = Arduino(USB_PORT)
        self.pin = board.get_pin('a:1:i')

    def getVoltage(self):
        value = self.pin.read()
        return value * 5000

    def getTemperature(self):
        voltage = self.getVoltage()
        temp = (voltage - 500) / 10
        return temp

    def isAboveThreshold(self):
        aboveThreshold = False

        if self.getTemperature() > self.MAX_TEMP:
            aboveThreshold = True

        return aboveThreshold
