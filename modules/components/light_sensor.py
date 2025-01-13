#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import smbus

rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

class LightSensor:
        address = None

        REG_ADDR_RESULT = 0x00
        REG_ADDR_ALERT  = 0x01
        REG_ADDR_CONFIG = 0x02
        REG_ADDR_LIMITL = 0x03
        REG_ADDR_LIMITH = 0x04
        REG_ADDR_HYST   = 0x05
        REG_ADDR_CONVL  = 0x06
        REG_ADDR_CONVH  = 0x07

        def __init__(self,address=0x55):
                self.address=address
                bus.write_byte_data(self.address, self.REG_ADDR_CONFIG,0x20)

        def adc_read(self):
                data=bus.read_i2c_block_data(self.address, self.REG_ADDR_RESULT, 2)
                raw_val=(data[0]&0x0f)<<8 | data[1]
                return raw_val

if __name__ == "__main__":
        adc= LightSensor()
        while True:
            print(adc.adc_read())
            time.sleep(.5)