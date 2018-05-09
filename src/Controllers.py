from src.ArduinoCom import *
from src.PiSensors import *
from src.Relay import *
import RPi.GPIO as GPIO
import time


class MotorController:

    def __init__(self):
        self.leftMotorPin = 35
        self.rightMotorPin = 36
        GPIO.setup(self.leftMotorPin, GPIO.OUT)
        GPIO.setup(self.rightMotorPin, GPIO.OUT)
        self.leftMotor = GPIO.PWM(self.leftMotorPin, 50)
        self.rightMotor = GPIO.PWM(self.rightMotorPin, 50)
        self.leftMotor.ChangeDutyCycle(0)
        self.rightMotor.ChangeDutyCycle(0)

    def setMotorSpeed(self, pwmDutyLeft, pwmDutyRight):
        self.leftMotor.ChangeDutyCycle(pwmDutyLeft)
        self.rightMotor.ChangeDutyCycle(pwmDutyRight)

    def stopMotors(self):
        self.leftMotor.ChangeDutyCycle(0)
        self.rightMotor.ChangeDutyCycle(0)


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
        self.motorController = MotorController()
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
                joyY = self.joystick.getY()
                self.setMotors(joyX, joyY)
            else:
                self.motorController.stopMotors()

            batteryFull = self.batterySensor.isFullyCharged()
            if batteryFull:
                self.stopCharging()

        else:
            self.fullStop()

    def setMotors(self, joyX, joyY):
        joyX *= 100
        joyY *= 100
        self.motorController.setMotorSpeed(joyX, joyY)

    def fullStop(self):
        self.relayController.closeAll()
        self.motorController.stopMotors()
        GPIO.cleanup()
        self.shutdown = True

    def stopCharging(self):
        pass


if __name__ == '__main__':

    if __package__ is None:
        __package__ = "src"

    GPIO.setmode(GPIO.BOARD)
    board = Arduino('/dev/ttyUSB0')
    leftMotorInput = board.get_pin('a:4:i')
    rightMotorInput = board.get_pin('a:5:i')
    try:
        mainController = MainController(board)
        while not mainController.shutdown:
            mainController.checkSensors()
            print("Left motor output voltage: " + str(leftMotorInput.read() * 5) + "\n" +
                  "Right motor output voltage: " + str(rightMotorInput.read() * 5) + "\n")
            time.sleep(0.2)
    finally:
        print("Shutdown")
        board.exit()
        GPIO.cleanup()
