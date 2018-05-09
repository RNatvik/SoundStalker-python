import RPi.GPIO as GPIO
import time


class SonicSensor:

    def __init__(self):
        self.triggerPin = 31    # 06
        self.echoPin = 32       # 12
        GPIO.setup(self.triggerPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)

    def trigger(self):
        GPIO.output(self.triggerPin, 1)
        time.sleep(0.000010)
        GPIO.output(self.triggerPin, 0)

    def waitForEcho(self):
        finished = False
        duration = 0
        timeout = time.time() + 0.5
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
        print("Before removal:")
        print(testResult)
        for test in testResult:
            if test > 50 or test == 0:
                testResult.remove(test)
        print("After removal:")
        print(testResult)
        totalValue = 0
        numberOfValues = 0
        for test in testResult:
            totalValue += test
            numberOfValues += 1
        print("total value: " + str(totalValue))
        print("number of values: " + str(numberOfValues))
        averageValue = totalValue / numberOfValues
        print("average value: " + str(averageValue))
        return averageValue

    def checkForObstacle(self):
        obstacle = False
        distance = self.getDistance()

        if distance < 20:
            obstacle = True

        return obstacle


if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BOARD)
        sonic = SonicSensor()
        while True:
            distance = sonic.getDistance()
            print(distance)
            time.sleep(0.2)
    finally:
        print("shutting down")
        GPIO.cleanup()