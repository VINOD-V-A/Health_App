import json
from kivymd.uix.screen import MDScreen

class NavigationDrawerScreen(MDScreen):
    pass


class Client_services(MDScreen):
    def __init__(self, **kwargs):
        super(Client_services, self).__init__(**kwargs)
        self.change()

    def change(self):
        with open('user_data.json', 'r') as file:
            user_info = json.load(file)
        self.ids.username.text = user_info['username']
        self.ids.email.text = user_info['email']

    def logout(self):
        logged_in_data = {'logged_in': False}
        with open("logged_in_data.json", "w") as json_file:
            json.dump(logged_in_data, json_file)

        self.manager.push_replacement("login")
        self.ids.nav_drawer.set_state("close")

    def home(self):
        self.ids.nav_drawer.set_state("close")

    def location_screen(self):
        self.manager.push("location")
