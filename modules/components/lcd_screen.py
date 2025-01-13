import time
import sys

if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

class Lcd_Screen:
    DISPLAY_RGB_ADDR = 0x62
    DISPLAY_TEXT_ADDR = 0x3e

    def __init__(self):
        self.bus = bus
        self.setRGB(255, 255, 255)

    def setRGB(self, r, g, b):
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 0, 0)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 1, 0)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 0x08, 0xaa)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 4, r)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 3, g)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 2, b)

    def textCommand(self, cmd):
        self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR, 0x80, cmd)

    def setText(self, text):
        self.textCommand(0x01)
        time.sleep(.05)
        self.textCommand(0x08 | 0x04)
        self.textCommand(0x28)
        time.sleep(.05)
        count = 0
        row = 0
        for c in text:
            if c == '\n' or count == 16:
                count = 0
                row += 1
                if row == 2:
                    break
                self.textCommand(0xc0)
                if c == '\n':
                    continue
            count += 1
            self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR, 0x40, ord(c))

    def setText_norefresh(self, text):
        self.textCommand(0x02)
        time.sleep(.05)
        self.textCommand(0x08 | 0x04)
        self.textCommand(0x28)
        time.sleep(.05)
        count = 0
        row = 0
        while len(text) < 32:
            text += ' '
        for c in text:
            if c == '\n' or count == 16:
                count = 0
                row += 1
                if row == 2:
                    break
                self.textCommand(0xc0)
                if c == '\n':
                    continue
            count += 1
            self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR, 0x40, ord(c))

    def create_char(self, location, pattern):
        location &= 0x07
        self.textCommand(0x40 | (location << 3))
        self.bus.write_i2c_block_data(self.DISPLAY_TEXT_ADDR, 0x40, pattern)

    def clear(self):
        self.setText("                                                            ")
    
    def display(self, text):
        self.clear()
        self.setText(text)


if __name__ == "__main__":
    lcd = Lcd_Screen()
    lcd.setText("Hello world\nThis is an LCD test")
    lcd.setRGB(0, 128, 64)
    time.sleep(2)
    for c in range(0, 20):
        lcd.setText_norefresh(f"Going to sleep in {c}...")
        lcd.setRGB(c, 20 - c, 0)
        time.sleep(0.1)
    lcd.setRGB(0, 0, 0)
    lcd.clear()