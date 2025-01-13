import json
import socket
from flask import Flask, jsonify, request
import threading
import subprocess
import time
from modules.components.button import Button
from modules.components.led_button import Led_Button
from modules.components.lcd_screen import Lcd_Screen
from modules.components.temperature_sensor import TemperatureHumidity_Sensor
from modules.components.hear_rate_sensor import MAX30100

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

def create_cron(title, date_time, url):
    try:
        cron_date1 = date_time.split("T")
        cron_date2 = cron_date1[0].split("-")
        cron_date3 = cron_date1[1].split(":")
        minute, hour, day, month = cron_date3[1], cron_date3[0], cron_date2[2], cron_date2[1]
        command = f"DISPLAY=:0 chromium-browser {url} &"
        cron_entry = f"{minute} {hour} {day} {month} * {command} # {title}\n"

        subprocess.run(f"(crontab -l; echo \"{cron_entry}\") | crontab -", shell=True, check=True)
        return {"status": "success", "message": f"Cron job '{title}' created successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def remove_cron(title):
    try:
        result = subprocess.run("crontab -l", shell=True, check=True, text=True, capture_output=True)
        cron_jobs = result.stdout.splitlines()

        filtered_jobs = [job for job in cron_jobs if f"{title}" not in job]

        subprocess.run(f"echo \"{chr(10).join(filtered_jobs)}\" | crontab -", shell=True, check=True)

        return {"status": "success", "message": "Cron job removed successfully"}

    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}


def modify_cron(title, new_date_time=None, new_url=None):
    try:
        result = subprocess.run("crontab -l", shell=True, check=True, text=True, capture_output=True)
        cron_jobs = result.stdout.splitlines()
        updated_jobs = []
        updated = False

        for job in cron_jobs:
            if len(str(job)) < 0:
                pass
            if f"# {title}" in job:
                cron_parts = job.split()
                if new_date_time:
                    cron_date1 = new_date_time.split("T")
                    cron_date2 = cron_date1.split("-")
                    cron_date3 = cron_date1.split(":")
                    minute, hour, day, month = cron_date3[1], cron_date3[0], cron_date2[2], cron_date2[1]
                if new_url:
                    command_index = job.index("chromium-browser")
                    cron_parts[command_index + 1] = new_url
                updated_jobs.append(" ".join(cron_parts))
                updated = True
            else:
                updated_jobs.append(job)

        if not updated:
            return {"status": "error", "message": f"No cron job found with title '{title}'"}

        subprocess.run(f"echo \"{chr(10).join(updated_jobs)}\" | crontab -", shell=True, check=True)
        return {"status": "success", "message": f"Cron job '{title}' modified successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

class MenuSystem:
    def __init__(self, button_next, button_prev, button_select_action, button_select_led):
        self.current_menu = "main"
        self.menu_index = 0
        self.load_contacts()
        self.menus = {
            "main": [
                {"label": "Check Device Status", "action": self.device_status},
                {"label": "Contacts", "action": self.contacts_menu},
                {"label": "Reset Host", "action": self.reset_host},
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
        temperature_sensor = TemperatureHumidity_Sensor()
        temperature = temperature_sensor.read()
        heartrate_sensor = MAX30100()
        heartrate = heartrate_sensor.read_heart_rate()
        return {"temperature": temperature, "heartrate": heartrate}

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

menu_system = MenuSystem(button_prev=5, button_select_action=17, button_select_led=16, button_next=18)

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

@app.route('/api/cron/create', methods=['POST'])
def api_create_cron():
    data = request.json
    title = data.get('title')
    date_time = data.get('date_time')
    url = data.get('url')

    if not title or not date_time or not url:
        return jsonify({"status": "error", "message": "Missing required parameters"}), 400

    result = create_cron(title, date_time, url)
    return jsonify(result)

@app.route('/api/cron/remove', methods=['POST'])
def api_remove_cron():
    data = request.json
    title = data.get('title')

    if not title:
        return jsonify({"status": "error", "message": "Missing required parameter: title"}), 400

    result = remove_cron(title)
    return jsonify(result)

@app.route('/api/cron/modify', methods=['POST'])
def api_modify_cron():
    data = request.json
    title = data.get('title')
    new_date_time = data.get('new_date_time')
    new_url = data.get('new_url')

    if not title:
        return jsonify({"status": "error", "message": "Missing required parameter: title"}), 400

    result = modify_cron(title, new_date_time, new_url)
    return jsonify(result)

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
