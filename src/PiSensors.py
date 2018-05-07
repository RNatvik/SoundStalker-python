import RPi.GPIO as GPIO
import time


class SonicSensor:

    def __init__(self):
        self.triggerPin = 31    #06
        self.echoPin = 32       #12
        GPIO.setup(self.triggerPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)

    def trigger(self):
        GPIO.output(self.triggerPin, 1)
        time.sleep(0.000010)
        GPIO.output(self.triggerPin, 0)

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
        timeout = time.time() + 3
        while not finished and time.time() < timeout:

            if GPIO.input(self.echoPin) == 1:
                startTime = time.time()

                while GPIO.input(self.echoPin) == 1:
                    finished = True
                else:
                    endTime = time.time()
                    duration = endTime - startTime

        return duration

    def getDistance(self):

        testResult = []

        for test in range(5):
            self.trigger()
            duration = self.waitForEcho()
            distance = duration * 1000000 * 0.034/2
            testResult.append(int(distance))

        for test in testResult:
            if test > 400:
                testResult.remove(test)

        totalValue = 0
        numberOfValues = 0
        for test in testResult:
            totalValue += test
            numberOfValues += 1

        averageValue = totalValue / numberOfValues
        return averageValue


if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BOARD)
        sonic = SonicSensor()
        while True:
            distance = sonic.getDistance()
            print(distance)
            # time.sleep()
    finally:
        print("shutting down")
        GPIO.cleanup()