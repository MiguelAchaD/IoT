import json
import socket
from flask import Flask, jsonify, request
import threading
import time
from modules.components.button import Button
from modules.components.led_button import Led_Button
from modules.components.temperature_sensor import TemperatureHumidity_Sensor
from modules.components.lcd_screen import Lcd_Screen

app = Flask(__name__)

IP_FILE = 'device_ip.json'
CONTACTS_FILE = 'contacts.json'

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]
    except:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def load_ip():
    try:
        with open(IP_FILE, 'r') as file:
            ip_data = json.load(file)
            if ip_data and 'ip' in ip_data:
                return ip_data['ip']
            else:
                return None
    except FileNotFoundError:
        return None

def save_ip(ip):
    with open(IP_FILE, 'w') as file:
        json.dump({"ip": ip}, file)

def delete_ip():
    try:
        with open(IP_FILE, 'w') as file:
            json.dump({"ip": None}, file)
    except Exception as e:
        print(f"Error al borrar la IP: {e}")

class MenuSystem:
    def __init__(self, button_next, button_prev, button_select_action, button_select_led, temperature_sensor):
        self.current_menu = "main"
        self.menu_index = 0
        self.temperature_sensor = temperature_sensor
        self.load_contacts()
        self.menus = {
            "main": [
                {"label": "Check Device Status", "action": self.device_status},
                {"label": "Contacts", "action": self.contacts_menu},
                {"label": "Reset Host", "action": self.reset_host},  # Nuevo ítem de menú
            ],
            "contacts": [
                {"label": "View Contacts", "action": self.view_contacts},
                {"label": "Back to Main Menu", "action": self.go_to_main},
            ],
            "view_contacts": [
                {"label": f"Contact: {contact}", "action": self.go_back_to_contacts}
                for contact in self.contacts
            ]
        }
        self.button_next = Button(button_next)
        self.button_select = Led_Button(button_select_action, button_select_led)
        self.ip_displayed = False
    
    def load_contacts(self):
        with open(CONTACTS_FILE, 'r') as f:
            self.contacts = json.load(f)

    def save_contacts(self):
        with open(CONTACTS_FILE, 'w') as f:
            json.dump(self.contacts, f)

    def show_menu(self):
        lcd_screen = Lcd_Screen()
        menu_items = self.menus[self.current_menu]
        menu_item_to_display = menu_items[self.menu_index]['label']
        lcd_screen.display(menu_item_to_display)

    def navigate_menu(self):
        try:
            while True:
                if self.button_next.is_pressed():
                    self.menu_index = (self.menu_index + 1) % len(self.menus[self.current_menu])
                    self.show_menu()
                    time.sleep(0.3)

                elif self.button_select.is_pressed():
                    action = self.menus[self.current_menu][self.menu_index]["action"]
                    action()
                    time.sleep(0.3)
        except KeyboardInterrupt:
            self.cleanup()

    def device_status(self):
        status = "OK"
        lcd_screen = Lcd_Screen()
        lcd_screen.display(status)
        return status

    def contacts_menu(self):
        self.current_menu = "contacts"
        self.menu_index = 0
        self.show_menu()

    def view_contacts(self):
        self.current_menu = "view_contacts"
        self.menu_index = 0
        self.show_menu()

    def go_back_to_contacts(self):
        self.current_menu = "contacts"
        self.menu_index = 0
        self.show_menu()

    def go_to_main(self):
        self.current_menu = "main"
        self.menu_index = 0
        self.show_menu()

    def reset_host(self):
        delete_ip()
        self.ip_displayed = False
        self.check_ip_and_show()
        self.current_menu = "main"
        self.menu_index = 0
        self.show_menu()

    def cleanup(self):
        self.button_next.cleanup()
        self.button_select.cleanup()

    def get_sensor_data(self):
        temperature = self.temperature_sensor.read_temperature()
        return {"temperature": temperature}

    def check_ip_and_show(self):
        device_ip = load_ip()
        if device_ip is None:
            device_ip = get_local_ip()
            print(f"Device IP: {device_ip}")
            lcd_screen = Lcd_Screen()
            lcd_screen.display(f"Device IP: {device_ip}")

            while not load_ip():
                time.sleep(5)

        if load_ip():
            self.ip_displayed = True

    def wait_for_ip(self):
        while not self.ip_displayed:
            time.sleep(1)

menu_system = MenuSystem(button_prev=5, button_select_action=17, button_select_led=16, button_next=18, temperature_sensor=TemperatureHumidity_Sensor())

@app.route('/api/status', methods=['GET'])
def api_status():
    client_ip = request.remote_addr

    if load_ip() is None:
        save_ip(client_ip)

    return jsonify({"status": "API is running!"})

@app.route('/api/sensors', methods=['GET'])
def api_sensors():
    sensor_data = menu_system.get_sensor_data()
    return jsonify(sensor_data)

def run_flask():
    app.run(host="0.0.0.0", port=5000)

def run_menu():
    menu_system.show_menu()
    menu_system.navigate_menu()
    menu_system.cleanup()

if __name__ == '__main__':
    try:
        ip_check_thread = threading.Thread(target=menu_system.check_ip_and_show)
        ip_check_thread.start()

        flask_thread = threading.Thread(target=run_flask)
        flask_thread.start()

        menu_system.wait_for_ip()

        menu_thread = threading.Thread(target=run_menu)
        menu_thread.start()

        flask_thread.join()
        menu_thread.join()
    finally:
        lcd_screen = Lcd_Screen()
        lcd_screen.setRGB(0, 0, 0)
        lcd_screen.clear()
