import RPi.GPIO as GPIO


class Relay:

    def __init__(self, relayPin):
        self.relayPin = relayPin
        GPIO.setup(self.relayPin, GPIO.OUT)

    def close(self):
        GPIO.output(self.relayPin, 0)

    def open(self):
        GPIO.output(self.relayPin, 1)
