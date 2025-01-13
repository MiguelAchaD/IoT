import RPi.GPIO as GPIO

class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_pressed(self):
        return GPIO.input(self.pin) == GPIO.HIGH

    def wait_for_press(self):
        while True:
            if self.is_pressed():
                return True

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        button = Button(18)
        button.wait_for_press()
    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        button.cleanup()
