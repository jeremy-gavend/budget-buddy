import mysql.connector, pygame
from Class_Sessions import Sessions
from Class_Operations import Operations
from Class_Buttons import Buttons, Textbox, Messages
from hashlib import sha256
import re

class App():
    def __init__(self):
        #----- Local connection stuffs
        self.mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            database = "budget_buddy"
        )
        self.cursor = self.mydb.cursor()
        #-----
        # Pygame inits
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen_size = (1200, 900)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.main_font = pygame.font.Font(None, 36)
        self.sort_font = pygame.font.Font(None, 18)
        pygame.display.set_caption("Budget Buddy")

        # Variables outside of loop
        self.running = True
        self.app_state = "login"
        # app_substate = "a"
        self.pepper = 'a' # stocked here, doesn't change
        
        # TODO can select a area that select the account, updating the display above (showing balance), highligting the row and show trnsactions
        # TODO (active account affects all requests (withdraw, sorts, etc))
        # TODO display the related transaction for a selected account
        ## Display: Text displays
        self.info_message = Messages((200, 800), (140, 32), color="orange", set_timeout=True)
        self.account_messages = {
            "username": Messages((50,50), (100, 32)),
            "balance": Messages((50,100), (100, 32))
        }
        self.tables = {
            "transactions": Messages((1000, 500), (400, 600)),
            "accounts": Messages((500, 500), (400, 600))
        }

        # Display: Login page (input fields + buttons) 
        self.login_textboxes = {
            "username": Textbox((300, 100), (200, 32), self.main_font, label='Username', label_font=self.main_font, tab_to="password"),
            "password": Textbox((300, 200), (200, 32), self.main_font, label='Password', label_font=self.main_font, tab_to="username")
        }

        ## Buttons
        self.login_buttons = {
            "login": Buttons((self.screen_size[0]*0.5, self.screen_size[1]-50), (200, 50), "LOGIN", self.main_font, link_to="main"),
            "register": Buttons((self.screen_size[0]*0.25, self.screen_size[1]-50), (200, 50), "REGISTER", self.main_font, link_to="register")
        }

        # Display: Register page (input fields + buttons)
        # TODO prevent overflow
        self.register_textboxes = {
            "last_name": Textbox((300, 100), (200, 32), self.main_font, label='Last Name', label_font=self.main_font, tab_to="first_name"),
            "first_name": Textbox((600, 100), (200, 32), self.main_font, label='First Name', label_font=self.main_font, tab_to="email"),
            "email": Textbox((300, 200), (200, 32), self.main_font, label='Email', label_font=self.main_font, tab_to="phone"),
            "phone": Textbox((600, 200), (200, 32), self.main_font, label='Phone', label_font=self.main_font, tab_to="username"),
            "username": Textbox((300, 300), (200, 32), self.main_font, label='Username', label_font=self.main_font, tab_to="password"),
            "password": Textbox((300, 400), (200, 32), self.main_font, label='Password', label_font=self.main_font, tab_to="confirm_password"),
            "confirm_password": Textbox((600, 400), (200, 32), self.main_font, label='Confirm Password', label_font=self.main_font, tab_to="last_name")
         }
        
        ### Buttons
        self.register_buttons = {
            "submit": Buttons((self.screen_size[0]*0.5, self.screen_size[1]-50), (200, 50), "SUBMIT", self.main_font, link_to="login"),
            "cancel": Buttons((self.screen_size[0]*0.25, self.screen_size[1]-50), (200, 50), "CANCEL", self.main_font, link_to="login")
        }

        # Display: Main page
        # Sort buttons
        # TODO function when clicked another time, it change asc to desc (sort_order = not sort order -> if sort_order then cursor.execute= [...] {sorting} sorting = "ASC;" else "DESC")
        self.main_sort_transactions_buttons = {
            "from": Buttons((100, 100), (100, 25), "FROM", self.sort_font),
            "to": Buttons((200, 100), (100, 25), "TO", self.sort_font),
            "amount": Buttons((300, 100), (100, 25), "AMOUNT", self.sort_font),
            "date": Buttons((400, 100), (100, 25), "DATE", self.sort_font),
            "type": Buttons((500, 100), (100, 25), "TYPE", self.sort_font),
            "category": Buttons((600, 100), (100, 25), "CATEGORY", self.sort_font)
        }

        # Filter buttons
        # TODO must be textbox and write the filter value directly
        # TODO if one label of date is empty, search for 1 date only
        # TODO place them below related sort buttons
        self.main_filter_transactions_buttons = {
            "dates": Textbox((100, 200), (100, 25), self.sort_font, tab_to="dates2"),
            "dates2": Textbox((150, 200), (100, 25), self.sort_font, tab_to="dates"),
            "from": Textbox((200, 200), (100, 25), self.sort_font, tab_to="to"),
            "to": Textbox((300, 200), (100, 25), self.sort_font, tab_to="from"),
            "amount": Textbox((400, 200), (100, 25), self.sort_font),
            "type": Textbox((500, 200), (100, 25), self.sort_font),
            "category": Textbox((600, 200), (100, 25), self.sort_font)
        }

        # Account buttons
        self.main_account_buttons = {
            "create": Buttons((50, 400), (100,25), "CREATE ACCOUNT", self.main_font),
            "delete": Buttons((100, 400), (100,25), "DELETE ACCOUNT", self.main_font)
        }

        # Operations buttons
        self.main_operation_buttons = {
            "deposit": Buttons((900, 100), (100, 25), "DEPOSIT", self.main_font),
            "withdraw": Buttons((1000, 100), (100, 25), "WITHDRAW", self.main_font),
            "transfert": Buttons((1100, 100), (100, 25), "TRANSFERT", self.main_font)
        }

        # Quit button
        self.main_buttons = {
            "logoff": Buttons((100, 700), (100, 25), "LOG OFF", self.main_font, link_to="login")
        }

        # TODO
        # SVG images
        # from __future__ import division
        # from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, parse_path
        # svg_path_button = "m 76,232.24998 c 81.57846,-49.53502 158.19366,-20.30271 216,27 61.26714, \
        #             59.36905 79.86223,123.38417 9,156 \
        #             -80.84947,31.72743 -125.19991,-53.11474 -118,-91 v 0"
        # path_button = parse_path(svg_path_button)
        # n_button = 100
        # svg_pts_button = [ (p.real,p.imag) for p in (path_button.point(i/n_button) for i in range(0, n_button+1))] 
        # pygame.draw.aalines()

    def start(self):
        while self.running:
            self.screen.fill((255, 255, 255))
            
            self.events(self.app_state)
            
            match self.app_state:
                case "login":
                    self.login()
                case "register":
                    self.register()
                case "main":
                    self.main()
                case _:
                    break
            
            self.clock.tick(60)
            pygame.display.flip()

        pygame.quit()

    def login(self):
        # Text field
        for index, button in self.login_textboxes.items():
            button.draw(self, index)

        ## Info message
        self.info_message.draw(self)

        ### Buttons
        for button in self.login_buttons.values():
            button.draw(self)
        
    def register(self):
        for index, button in self.register_textboxes.items():
            button.draw(self, index)

        ## Messages
        self.info_message.draw(self)

        ### Buttons
        for button in self.register_buttons.values():
            button.draw(self)

    def main(self):

        # !
        # TODO create lines around each lines

        # TODO account display (+ username)
        # [TOP-LEFT]
        self.account_messages["balance"].text = self.user.get_balance(self.cursor)
        for message in self.account_messages.values():
            message.draw(self)

        for index, button in self.main_account_buttons.items():
            button.draw(self)

        # TODO Either display all accounts and transfert by id to id, or select an account and display it, then transfert from it

        #[BOTTOM-LEFT]
        for table, rows in self.tables.items():
            self.convert_table_to_row(table, rows.text, self.user)
            rows.draw(self)

        
        # TODO Accounts lists (selectable)


        # TODO self.active, need to change color when active
      
        #[TOP-RIGHT]
        # TODO Transaction actions (sub_state)
        for button in self.main_operation_buttons.values():
            button.draw(self)
        #[BOTTOM-RIGHT]
        # Sort buttons
        for button in self.main_sort_transactions_buttons.values():
            button.draw(self)
        # TODO Transaction list display
        
        ## Messages
        self.info_message.draw(self)

        ### Quit button
        for button in self.main_buttons.values():
            button.draw(self)

    def verif_login(self):
        self.cursor.execute(f"SELECT salt FROM users WHERE username = '{self.login_textboxes["username"].text}';")
        try:
            salt = self.cursor.fetchall()[0][0]
            raw_password = self.pepper + self.login_textboxes["password"].text + salt
            password = sha256(raw_password.encode()).hexdigest()

            self.cursor.execute(f"SELECT id, username FROM users WHERE username = '{self.login_textboxes["username"].text}' AND password = '{password}';")
            user_data = self.cursor.fetchall()

            if bool(user_data):
                return user_data[0][0], user_data[0][1]
        except Exception:
            self.info_message.text = ["Error in retriving user data!"]
        return False

    def login_failed(self):
        self.info_message.text = ["Login failed! Please verify if the username or password is correct"]

    def create_session(self, user_data):
        self.user = Sessions.create_session(user_data)
        self.account_messages["username"].text = [self.user.username]

    def create_account(self):
        """Called when clicking "submit" in register menu"""
        for index, textbox in self.register_textboxes.items():
            if not textbox.text:
                self.info_message.text = ["Please fill all the forms"]
                return False
            elif not self.is_valid(index, textbox.text):
                self.info_message.text = [f"{index.capitalize()} not valid!"]
                if index == "password":
                    self.info_message.text = ["Password must be 10 to 99 characters long, contain 1 uppercase letter,", "1 lowercase letter, a number and a special symbol!"]
                return False
            elif index == "password":
                if textbox.text != self.register_textboxes["confirm_password"].text:
                    self.info_message.text = ["Passwords must be the same!"]
                    return False
            elif index == "username":
                if self.username_exists(textbox.text):
                    self.info_message.text = ["Username already exists!"]
                    return False
        
        salt = 'b'
        username = self.register_textboxes["username"].text
        raw_password = self.pepper + self.register_textboxes["password"].text + salt
        password = sha256(raw_password.encode()).hexdigest()
        last_name = self.register_textboxes["last_name"].text
        first_name = self.register_textboxes["first_name"].text
        email = self.register_textboxes["email"].text
        phone = self.register_textboxes["phone"].text

        self.cursor.execute(f"INSERT INTO users (username, password, salt, last_name, first_name, email, phone) \
                                VALUES ('{username}', '{password}', '{salt}', '{last_name}', '{first_name}', '{email}', '{phone}');")
        self.mydb.commit()
        return True

    def is_valid(self, index, text):
        # TODO fix invalid escape sequence
        if index == "email":
            regex_pattern = re.compile('^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$')
        elif index == "phone":
            regex_pattern = re.compile('^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$')
        elif index == "password":
            regex_pattern = re.compile('^(?=\S{10,99}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')        
        else:
            return True
        return regex_pattern.match(text)

    def username_exists(self, text):
        self.cursor.execute(f"SELECT username FROM users where username = '{text}'")
        return self.cursor.fetchall()
    
    def convert_table_to_row(self, table, value, user):
        # TODO make it so the username appear in place of user_id (from and to)
        self.cursor.execute(f"SELECT * FROM {table} WHERE user_id = {user.user_id}")
        # TODO condition to select the "to user" and display it
        rows = self.cursor.fetchall()
        value = []
        for row in rows:
            value.append(f"{row[0]} | {row[1]} | {row[2]}| {row[3]} | {row[4]} | | {row[5]}")

    def events(self, app_state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if app_state == "login":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for textbox in self.login_textboxes.values():
                        if textbox.rect.collidepoint(event.pos):
                            textbox.active = True 
                        else:
                            textbox.active = False
                    
                    for index, button in self.login_buttons.items():
                        if button.rect.collidepoint(event.pos):
                            if index == "login": 
                                logged_user = self.verif_login()
                                if logged_user:
                                    self.create_session(logged_user)
                                    self.login_textboxes["password"].text = '' # To delete the password in the field once sucessfully connected
                                    self.login_textboxes["password"].text_spoof = '' # To delete the stars in the sky
                                    self.app_state = button.link_to
                                    break
                                else:
                                    self.login_failed()
                                    break
                            else:
                                self.app_state = button.link_to
                                break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        logged_user = self.verif_login()
                        if logged_user:
                            self.create_session(logged_user)
                            self.login_textboxes["password"].text = '' #To delete the password in the field once sucessfully connected
                            self.app_state = "main"
                        else:
                            self.login_failed()
                    else:
                        for index, textbox in self.login_textboxes.items():
                            if textbox.active:
                                if event.key == pygame.K_BACKSPACE:
                                    textbox.text = textbox.text[:-1]
                                    if index == "password" or index == "confirm_password":
                                        textbox.text_spoof = textbox.text_spoof[:-1]
                                    break
                                elif event.key == pygame.K_TAB:
                                    textbox.active = False
                                    self.login_textboxes[textbox.tab_to].active = True
                                    break
                                else:
                                    previous_lenght = len(textbox.text)
                                    textbox.text += event.unicode
                                    if index == "password" or index == "confirm_password":
                                        for i in range(len(textbox.text) - previous_lenght):
                                            textbox.text_spoof += "*"
                                    break

            if app_state == "register":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for textbox in self.register_textboxes.values():
                        if textbox.rect.collidepoint(event.pos):
                            textbox.active = True 
                        else:
                            textbox.active = False

                    for index, button in self.register_buttons.items():
                        if button.rect.collidepoint(event.pos):
                            if index == "submit": 
                                if self.create_account():
                                    self.app_state = button.link_to
                            else:
                                self.app_state = button.link_to

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.create_account():
                            self.app_state = "login"
                    else:
                        for index, textbox in self.register_textboxes.items():
                            if textbox.active:
                                if event.key == pygame.K_BACKSPACE:
                                    textbox.text = textbox.text[:-1]
                                    if index == "password" or index == "confirm_password":
                                        textbox.text_spoof = textbox.text_spoof[:-1]
                                    break
                                elif event.key == pygame.K_TAB:
                                    textbox.active = False
                                    self.register_textboxes[textbox.tab_to].active = True
                                    break
                                else:
                                    previous_lenght = len(textbox.text)
                                    textbox.text += event.unicode
                                    if index == "password" or index == "confirm_password":
                                        for i in range(len(textbox.text) - previous_lenght):
                                            textbox.text_spoof += "*"
                                    break

            if self.app_state == "main":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for index, button in self.main_buttons.items():
                        if button.rect.collidepoint(event.pos):
                            self.app_state = button.link_to
                    for index, button in self.main_sort_transactions_buttons.items():
                        if button.rect.collidepoint(event.pos):
                            self.tables["transactions"].text = self.user.sort_by(self.cursor, "transactions", index, True)
                    for index, button in self.main_account_buttons.items():
                        if button.rect.collidepoint(event.pos):
                            Operations.manage_account(self, index)  
                    for index, button in self.main_operation_buttons.items():
                        if button.rect.collidepoint(event.pos):
                            Operations.operation(self, index)           




# --- Test ---
# --- ---- ---

#for creating an account (user can have several)
#this goes in a "create an bank account" button
                # try:
                #     self.user.account_creation(cursor, mydb)
                # except Exception:
                #     self.message_text = "Error in account creation"


# ---Tests---
# print in textbox
# balance = user.get_balance(cursor)

#button deposit that display deposit interface
# message_dep = Operations.deposit(cursor, mydb, user, 100, "Test_deposit", "None")
# print(message_dep)

#button withdraw that display withdraw interface
# message_withd = Operations.withdraw(cursor, mydb, user, 50, "Test_withdraw", "None")
# print(message_withd)


#button history that display history interface
# historic = Operations.history(cursor, user)
# print(historic)

# lots of button that call this but with different labels
# sorted = user.sort_by(cursor, "date", True)
# print(sorted)

# for specific dates button
# sorted_dates = user.sort_dates(cursor, "2021-01-01", "2021-12-31")
# print(sorted_dates)

# sorted_dates = user.sort_dates(cursor, "2021-01-01")
# print(sorted_dates)