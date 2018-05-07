import RPi.GPIO as GPIO


class SonicSensor:

    def __init__(self):
        self.triggerPin = 31
        self.echoPin = 32
        GPIO.setup(self.triggerPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)

    def trigger(self):
        pass

    def waitForEcho(self):
        pass

    def getDistance(self):
        self.trigger()

    def shitTestForRuben(self):
        if GPIO.input(self.echoPin):
            GPIO.output(self.triggerPin, 1)
        else:
            GPIO.output(self.triggerPin, 0)