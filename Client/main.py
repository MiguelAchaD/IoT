import keyboard

class MenuSystem:
    def __init__(self):
        self.current_menu = "main"
        self.menu_index = 0
        self.menus = {
            "main": [
                {"label": "Contacts", "action": self.contacts_menu},
                {"label": "Check Heartrate", "action": self.check_heartrate},
                {"label": "Check Device Status", "action": self.device_status},
            ],
            "contacts": [
                {"label": "Add Contact", "action": self.add_contact},
                {"label": "View Contacts", "action": self.view_contacts},
                {"label": "Back to Main Menu", "action": self.go_to_main},
            ],
        }
        self.scan_codes = {
            "right": 77,
            "left": 75,
            "enter": 28,
        }

    def show_menu(self):
        menu_items = self.menus[self.current_menu]
        print("\n" + "=" * 30)
        print(f"Current Menu: {self.current_menu}")
        for i, item in enumerate(menu_items):
            if i == self.menu_index:
                print(f"--> {item['label']}")
            else:
                print(f"    {item['label']}")
        print("=" * 30)

    def navigate_menu(self, event):
        if event.event_type == "down":
            menu_items = self.menus[self.current_menu]
            if event.scan_code == self.scan_codes["right"]:
                self.menu_index = (self.menu_index + 1) % len(menu_items)
            elif event.scan_code == self.scan_codes["left"]:
                self.menu_index = (self.menu_index - 1) % len(menu_items)
            elif event.scan_code == self.scan_codes["enter"]:
                menu_items[self.menu_index]["action"]()
            self.show_menu()

    def run(self):
        print("Use the arrow keys to navigate and Enter to select.")
        self.show_menu()
        keyboard.hook(self.navigate_menu)
        keyboard.wait("esc")

    def contacts_menu(self):
        self.current_menu = "contacts"
        self.menu_index = 0
        self.show_menu()

    def check_heartrate(self):
        print("\n[INFO] Checking heart rate...")
        input("Press Enter to return to the menu.")
        self.show_menu()

    def device_status(self):
        print("\n[INFO] Checking device status...")
        input("Press Enter to return to the menu.")
        self.show_menu()

    def add_contact(self):
        print("\n[INFO] Adding a contact...")
        input("Press Enter to return to the menu.")
        self.show_menu()

    def view_contacts(self):
        print("\n[INFO] Viewing contacts...")
        input("Press Enter to return to the menu.")
        self.show_menu()

    def go_to_main(self):
        self.current_menu = "main"
        self.menu_index = 0
        self.show_menu()

menu_system = MenuSystem()
menu_system.run()
