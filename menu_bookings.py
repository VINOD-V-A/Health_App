from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen



class Booking(MDScreen):

    def booking_back(self):
        self.manager.pop()
        screen = self.manager.get_screen('client_services')
        screen.ids.nav_drawer.set_state("close")
