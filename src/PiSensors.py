import RPi.GPIO as GPIO
import time


class SonicSensor:

    def __init__(self):
        self.triggerPin = 31
        self.echoPin = 32
        GPIO.setup(self.triggerPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)

    def trigger(self):
        GPIO.output(self.triggerPin, 1)
        time.sleep(0.000010)
        GPIO.output(self.triggerPin, 0)

    def waitForEcho(self):
        GPIO.wait_for_edge(self.echoPin, GPIO.RISING)
        startTime = time.time()
        GPIO.wait_for_edge(self.echoPin, GPIO.FALLING)
        endTime = time.time()
        duration = endTime - startTime
        return duration

    def getDistance(self):
        self.trigger()
        duration = self.waitForEcho()
        distance = duration * 0.034/2
        return distance


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    sonic = SonicSensor()
    try:
        while True:
            distance = sonic.getDistance()
            print(distance)
    finally:
        GPIO.cleanup()