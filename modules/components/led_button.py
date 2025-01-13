import RPi.GPIO as GPIO
from time import sleep

class Led_Button:
    def __init__(self, pin_button, pin_led):
        self.pin_button = pin_button
        self.pin_led = pin_led
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pin_led, GPIO.OUT)
        GPIO.output(self.pin_led, GPIO.HIGH)

    def is_pressed(self):
        return GPIO.input(self.pin_button) == GPIO.LOW

    def wait_for_press(self):
        sleep(1)
        while True:
            if self.is_pressed():
                return True

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        led_button = Led_Button(17, 16)
        led_button.wait_for_press()
    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        led_button.cleanup()
