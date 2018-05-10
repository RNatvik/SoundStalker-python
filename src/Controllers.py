from ArduinoCom import *
from PiSensors import *
from Relay import *
import RPi.GPIO as GPIO
import time


class MotorController:

    def __init__(self, arduino, leftMotorPin, rightMotorPin):
        board = arduino
        self.iterator = util.Iterator(board)
        self.iterator.setDaemon(True)
        self.iterator.start()
        self.leftMotor = Motor(board, leftMotorPin)
        self.rightMotor = Motor(board, rightMotorPin)

    def setMotorSpeed(self, value):
        leftSpeed = self.calculateLeftSpeed(value)
        rightSpeed = self.calculateRightSpeed(value)
        self.leftMotor.setSpeed(leftSpeed)
        self.rightMotor.setSpeed(rightSpeed)

    # if value == 1, return 100
    # if value == -1, return 0
    # if value == 0, return 50
    def calculateLeftSpeed(self, value):
        value += 1
        value *= 100
        value /= 2
        return value

    # if value == 1, return 0
    # if value == -1, return 100
    # if value == 0, return 50
    def calculateRightSpeed(self, value):
        value -= 1
        value *= -100
        value /= 2
        return value

    def stopMotors(self):
        pass


class RelayController:

    def __init__(self):
        self.chargeRelay = Relay(11)
        self.relay2 = Relay(12)
        self.relay3 = Relay(13)
        self.relay4 = Relay(15)
        self.relay5 = Relay(16)

    def closeAll(self):
        self.chargeRelay.close()
        self.relay2.close()
        self.relay3.close()
        self.relay4.close()
        self.relay5.close()

    def openAll(self):
        self.chargeRelay.open()
        self.relay2.open()
        self.relay3.open()
        self.relay4.open()
        self.relay5.open()


class MainController:

    def __init__(self, arduino):
        self.shutdown = False
        board = arduino
        self.motorController = MotorController(board, 'd:10:p', 'd:11:p')
        self.relayController = RelayController()
        self.sonicSensor = SonicSensor()
        self.batterySensor = BatterySensor(board, 'a:0:i')
        self.tempSensor = TempSensor(board, 'a:1:i')
        self.joystick = Joystick(board, 'a:2:i', 'a:3:i')

    def checkSensors(self):

        batteryDepleted = self.batterySensor.isDepleted()
        tempAboveThreshold = self.tempSensor.isAboveThreshold()

        if not (tempAboveThreshold or batteryDepleted):

            obstacleFound = self.sonicSensor.checkForObstacle()
            if not obstacleFound:
                joyX = self.joystick.getX()
                self.motorController.setMotorSpeed(joyX)
            else:
                self.motorController.stopMotors()

            batteryFull = self.batterySensor.isFullyCharged()
            if batteryFull:
                self.stopCharging()

        else:
            self.fullStop()

    def fullStop(self):
        self.relayController.openAll()
        self.motorController.stopMotors()
        self.shutdown = True

    def stopCharging(self):
        pass


if __name__ == '__main__':

    if __package__ is None:
        __package__ = "src"

    GPIO.setmode(GPIO.BOARD)
    board = Arduino('/dev/ttyUSB0')

    try:
        mainController = MainController(board)
        leftMotorInput = board.get_pin('a:4:i')
        rightMotorInput = board.get_pin('a:5:i')
        print("Sleeping")
        time.sleep(3)
        print("Awake")
        while not mainController.shutdown:
            mainController.checkSensors()
            print("Left motor output voltage: " + str(leftMotorInput.read() * 5) + "\n" +
                  "Right motor output voltage: " + str(rightMotorInput.read() * 5) + "\n")
            time.sleep(0.2)
    finally:
        print("Shutdown")
        board.exit()
        GPIO.cleanup()
