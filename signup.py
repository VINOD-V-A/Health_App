import os
import sqlite3
import re
import anvil
import requests
from anvil import Timer
from anvil.tables import app_tables
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from twilio.rest import Client

# SQLite database setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        phone TEXT NOT NULL,
        pincode TEXT NOT NULL
    )
''')
conn.commit()


class Signup(MDScreen):

    # def google_sign_in(self):
    #     # Set up the OAuth 2.0 client ID and client secret obtained from the Google Cloud Console
    #     client_id = "749362207551-tdoq2d8787csqqnbvpdgcc3m2sdtsnd1.apps.googleusercontent.com"
    #     client_secret = "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"
    #     redirect_uri = "https://oxivive.com/oauth/callback"
    #     redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    #
    #     # Set up the Google OAuth flow
    #     flow = InstalledAppFlow.from_client_secrets_file(
    #         "client_secret.json",
    #         scopes=["https://www.googleapis.com/auth/userinfo.email"],
    #         redirect_uri=redirect_uri
    #     )
    #
    #     # Get the authorization URL
    #     auth_url, _ = flow.authorization_url(prompt="select_account")
    #     print(f"Authorization URL: {auth_url}")
    #
    #     # Open a web browser to the authorization URL
    #     webbrowser.open(auth_url)
    #
    #     # Get the authorization code from the user
    #     authorization_code = input("Enter the authorization code: ")
    #
    #     # Exchange the authorization code for credentials
    #     credentials = flow.fetch_token(
    #         token_uri="https://oauth2.googleapis.com/token",
    #         authorization_response=authorization_code
    #     )
    #
    #     # Use the obtained credentials for further Google API requests
    #     # Example: print the user's email address
    #     user_email = credentials.id_token["email"]
    #     print(f"User email: {user_email}")
    #
    # def exchange_code_for_tokens(self, authorization_code):
    #     token_url = "https://oauth2.googleapis.com/token"
    #
    #     params = {
    #         "code": authorization_code,
    #         "client_id": "your_client_id",
    #         "client_secret": "your_client_secret",
    #         "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    #         "grant_type": "authorization_code"
    #     }
    #
    #     response = requests.post(token_url, data=params)
    #     token_data = response.json()
    #
    #     return token_data
    def is_connected(self):
        try:
            # Attempt to make a simple HTTP request to check connectivity
            response = requests.get('https://www.google.com', timeout=1)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return True
        except requests.RequestException:
            return False

    def get_database_connection(self):
        if self.is_connected():
            # Use Anvil's database connection
            return anvil.server.connect("server_UY47LMUKBDUJMU4EA3RKLXCC-LP5NLIEYMCLMZ4NU")
        else:
            # Use SQLite database connection
            return sqlite3.connect('users.db')

    def show_validation_dialog(self, message):
        # Create the dialog asynchronously
        Clock.schedule_once(lambda dt: self._create_dialog(message), 0)

    def _create_dialog(self, message):
        dialog = MDDialog(
            text=f"{message}",
            elevation=0,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

    def users(self, instance, *args):

        username = self.ids.signup_username.text
        email = self.ids.signup_email.text
        password = self.ids.signup_password.text
        phone = self.ids.signup_phone.text
        pincode = self.ids.signup_pincode.text

        # Validation logic
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        # Enhanced password validation
        is_valid_password, password_error_message = self.validate_password(password)
        # Clear existing helper texts
        self.ids.signup_username.helper_text = ""
        self.ids.signup_email.helper_text = ""
        self.ids.signup_password.helper_text = ""
        self.ids.signup_phone.helper_text = ""
        self.ids.signup_pincode.helper_text = ""
        if not username:
            self.ids.signup_username.error = True
            self.ids.signup_username.helper_text = "Enter Name"
        elif not email or not re.match(email_regex, email):
            self.ids.signup_email.error = True
            self.ids.signup_email.helper_text = "Invalid Email"
        elif not is_valid_password:
            self.ids.signup_password.error = True
            self.ids.signup_password.helper_text = password_error_message
        elif not phone or len(phone) != 10:
            self.ids.signup_phone.error = True
            self.ids.signup_phone.helper_text = "Invalid Phone number (10 digits required)"
        elif not pincode or len(pincode) != 6:
            self.ids.signup_pincode.error = True
            self.ids.signup_pincode.helper_text = "Invalid Pincode (6 digits required)"

        else:
            # Clear any existing errors and helper texts
            self.ids.signup_username.error = False
            self.ids.signup_username.helper_text = ""
            self.ids.signup_email.error = False
            self.ids.signup_email.helper_text = ""
            self.ids.signup_password.error = False
            self.ids.signup_password.helper_text = ""
            self.ids.signup_phone.error = False
            self.ids.signup_phone.helper_text = ""
            self.ids.signup_pincode.error = False
            self.ids.signup_pincode.helper_text = ""

            # clear input texts
            self.ids.signup_username.text = ""
            self.ids.signup_email.text = ""
            self.ids.signup_password.text = ""
            self.ids.signup_phone.text = ""
            self.ids.signup_pincode.text = ""

            # If validation is successful, insert into the database
            try:
                if self.is_connected():
                    anvil.server.connect("server_UY47LMUKBDUJMU4EA3RKLXCC-LP5NLIEYMCLMZ4NU")
                    rows = app_tables.users.search()
                    # Get the number of rows
                    id = len(rows) + 1
                    app_tables.users.add_row(
                        id=id,
                        username=username,
                        email=email,
                        password=password,
                        phone=float(phone),
                        pincode=int(pincode))
                    connection = sqlite3.connect('users.db')
                    cursor = connection.cursor()
                    cursor.execute('''
                                    INSERT INTO users (username, email, password, phone, pincode)
                                    VALUES (?, ?, ?, ?, ?)
                                ''', (username, email, password, phone, pincode))
                    connection.commit()
                    connection.close()
                else:
                    self.show_validation_dialog("No internet connection")

            except Exception as e:
                print(e)
                self.show_validation_dialog("No internet connection")
            # Navigate to the success screen
            self.manager.push("login")

    # password validation
    def validate_password(self, password):
        # Check if the password is not empty
        if not password:
            return False, "Password cannot be empty"
        # Check if the password has at least 8 characters
        if len(password) < 6:
            return False, "Password must have at least 6 characters"
        # Check if the password contains both uppercase and lowercase letters
        if not any(c.isupper() for c in password) or not any(c.islower() for c in password):
            return False, "Password must contain uppercase, lowercase"
        # Check if the password contains at least one digit
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        # Check if the password contains at least one special character
        special_characters = r"[!@#$%^&*(),.?\":{}|<>]"
        if not re.search(special_characters, password):
            return False, "Password must contain a special character"
        # All checks passed; the password is valid
        return True, "Password is valid"
