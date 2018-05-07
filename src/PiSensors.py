import RPi.GPIO as GPIO
import time


class SonicSensor:

    def __init__(self):
        self.triggerPin = 31
        self.echoPin = 32
        GPIO.setup(self.triggerPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)

    def trigger(self):
        print("Trigger start")
        GPIO.output(self.triggerPin, 1)
        time.sleep(0.000010)
        GPIO.output(self.triggerPin, 0)
        print("trigger end")

    # def waitForEcho(self):
    #     print("wait for edge start")
    #     GPIO.wait_for_edge(self.echoPin, GPIO.RISING, timeout=5000)
    #     print("found rising edge")
    #     startTime = time.time()
    #     print("waiting for falling edge")
    #     GPIO.wait_for_edge(self.echoPin, GPIO.FALLING, timeout=5000)
    #     print("found falling edge")
    #     endTime = time.time()
    #     duration = endTime - startTime
    #     print("duration: " + duration)
    #     return duration

    def waitForEcho(self):
        finished = False
        duration = 0

        while not finished:

            if GPIO.input(self.echoPin) == 1:
                startTime = time.time()

                while GPIO.input(self.echoPin) == 1:
                    finished = True
                else:
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
        print("shutting down")
        GPIO.cleanup()