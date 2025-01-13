import Adafruit_DHT
import time

class TemperatureHumidity_Sensor:
    def __init__(self, sensor=Adafruit_DHT.DHT11, pin=12):
        self.sensor = sensor
        self.pin = pin

    def read(self):
        try:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
            if temperature is not None:
                return temperature
            else:
                raise ValueError("No se pudo leer del sensor.")
        except Exception as e:
            return None, None


if __name__ == "__main__":
    try:
        dht_sensor = TemperatureHumidity_Sensor(pin=12)

        while True:
            temperature = dht_sensor.read()
            if temperature is not None:
                print(f"Temperatura: {temperature:.2f} °C")
            else:
                print("Error al leer los datos del sensor.")
            time.sleep(2)

    except KeyboardInterrupt:
        print("Saliendo del programa.")
