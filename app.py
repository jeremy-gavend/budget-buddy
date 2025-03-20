import mysql.connector, pygame
from Class_Sessions import Sessions
from Class_Operations import Operations
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
        
        ## Display: Info messages
        self.message_text = ''
        self.message_text2 = '' #second line for too much text

        # Display: Login page (input fields + buttons) 
        self.login_username_input_field = pygame.Rect(300, 100, 140, 32)
        self.login_username_field_active = False
        self.login_username_input = ''

        self.login_username_label = self.main_font.render("Username", True, "black")

        self.login_password_input_field = pygame.Rect(300, 200, 140, 32)
        self.login_password_field_active = False
        self.login_password_input = ''
        self.login_password_input_spoof = ''

        self.login_password_label = self.main_font.render("Password", True, "black")

        ## Buttons
        self.login_button = pygame.Rect(self.screen_size[0]*0.5, self.screen_size[1]-50, 200, 50)
        self.login_button_text = self.main_font.render("Login", True, (0, 0, 0))

        self.register_button = pygame.Rect(self.screen_size[0]*0.25, self.screen_size[1]-50, 200, 50)
        self.register_button_text = self.main_font.render("Register", True, (0, 0, 0))

        # Display: Register page (input fields + buttons)
        # TODO refractor this in a loop
        self.register_last_name_input_field = pygame.Rect(300, 100, 140, 32)
        self.register_last_name_field_active = False
        self.register_last_name_input = ''
        
        self.register_last_name_label = self.main_font.render("Last Name", True, "black")

        self.register_first_name_input_field = pygame.Rect(500, 100, 140, 32)
        self.register_first_name_field_active = False
        self.register_first_name_input = ''

        self.register_first_name_label = self.main_font.render("First Name", True, "black")

        self.register_email_input_field = pygame.Rect(300, 200, 140, 32)
        self.register_email_field_active = False
        self.register_email_input = ''

        self.register_email_label = self.main_font.render("Email", True, "black")

        self.register_phone_input_field = pygame.Rect(500, 200, 140, 32)
        self.register_phone_field_active = False
        self.register_phone_input = ''

        self.register_phone_label = self.main_font.render("Phone", True, "black")

        # Login related
        self.register_username_input_field = pygame.Rect(300, 300, 140, 32)
        self.register_username_field_active = False
        self.register_username_input = ''

        self.register_username_label = self.main_font.render("Username", True, "black")

        self.register_password_input_field = pygame.Rect(300, 400, 140, 32)
        self.register_password_field_active = False
        self.register_password_input = ''

        self.register_password_label = self.main_font.render("Password", True, "black")

        self.register_confirm_password_input_field = pygame.Rect(500, 400, 140, 32)
        self.register_confirm_password_field_active = False
        self.register_confirm_password_input = ''

        self.register_confirm_password_label = self.main_font.render("Confirm Password", True, "black")

        ### Buttons
        self.submit_button = pygame.Rect(self.screen_size[0]*0.5, self.screen_size[1]-50, 200, 50)
        self.submit_button_text = self.main_font.render("Submit", True, (0, 0, 0))

        self.cancel_button = pygame.Rect(self.screen_size[0]*0.25, self.screen_size[1]-50, 200, 50)
        self.cancel_button_text = self.main_font.render("Cancel", True, (0, 0, 0))

        # Display: Main page

        # Tables 
        self.main_account_table = []
        self.main_transaction_table = []

        # Sort buttons
        # TODO function when clicked another time, it change asc to desc (sort_order = not sort order -> if sort_order then cursor.execute= [...] {sorting} sorting = "ASC;" else "DESC")
        self.main_sort_button_from = pygame.Rect(100, 100, 100, 25)
        self.main_sort_button_from_text = self.sort_font.render('FROM', True, (0, 0, 0))
        
        self.main_sort_button_to = pygame.Rect(200, 100, 100, 25)
        self.main_sort_button_to_text = self.sort_font.render('TO', True, (0, 0, 0))
        
        self.main_sort_button_amount = pygame.Rect(300, 100, 100, 25)
        self.main_sort_button_amount_text = self.sort_font.render('AMOUNT', True, (0, 0, 0))
        
        self.main_sort_button_date = pygame.Rect(400, 100, 100, 25)
        self.main_sort_button_date_text = self.sort_font.render('DATE', True, (0, 0, 0))

        self.main_sort_button_type = pygame.Rect(500, 100, 100, 25)
        self.main_sort_button_type_text = self.sort_font.render('TYPE', True, (0, 0, 0))

        self.main_sort_button_category = pygame.Rect(600, 100, 100, 25)
        self.main_sort_button_category_text = self.sort_font.render('CATEGORY', True, (0, 0, 0))

        self.main_filter_dates_button = pygame.Rect(700, 100, 100, 25)
        self.main_filter_dates_button_text = self.sort_font.render('DATES...', True, (0, 0, 0))

        # Quit button
        self.main_logoff_button = pygame.Rect(100, 700, 100, 25)
        self.main_logoff_button_text = self.main_font.render('LOG OFF', True, (0, 0, 0))

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
        if self.login_username_field_active:
            login_username_field_color = 'lightblue'
        else:
            login_username_field_color = 'lightgray'

        if self.login_password_field_active:
            login_password_field_color = 'lightblue'
        else:
            login_password_field_color = 'lightgray'

        # Label: Username
        self.screen.blit(self.login_username_label, pygame.Rect(300, 50, 140, 32)) # TODO relative to the box it belong
        # Field: Username
        pygame.draw.rect(self.screen, login_username_field_color, self.login_username_input_field)
        self.login_username_button_label_render = self.main_font.render(self.login_username_input, True, "black")
        self.screen.blit(self.login_username_button_label_render,self.login_username_input_field)

        # Label: Password
        self.screen.blit(self.login_password_label, pygame.Rect(300, 150, 140, 32)) # TODO relative to the box it belong
        # Field: Password
        pygame.draw.rect(self.screen, login_password_field_color, self.login_password_input_field)
        self.login_password_button_label_render = self.main_font.render(self.login_password_input_spoof, True, "black")
        self.screen.blit(self.login_password_button_label_render,self.login_password_input_field)

        ## Info message
        # TODO put a timer that makes this clear after x frames        
        self.login_information = self.main_font.render(self.message_text, True, "orange")
        self.screen.blit(self.login_information, pygame.Rect(200, 800, 140, 32))
        
        self.login_information2 = self.main_font.render(self.message_text2, True, "orange")
        self.screen.blit(self.login_information2, pygame.Rect(200, 820, 140, 32))

        # TODO make a class or a function that give another color depending of the error (but edit the same text)
        # self.login_error = self.main_font.render(self.message_text, True, "red")
        # self.screen.blit(self.login_error, pygame.Rect(200, 800, 140, 32))

        ### Buttons
        self.screen.blit(self.login_button_text, self.login_button)
        self.screen.blit(self.register_button_text, self.register_button)

    def register(self):
        # TODO refractor this (to change color when it's active/unactive)
        if self.register_last_name_field_active:
            register_last_name_field_color = 'lightblue'
        else:
            register_last_name_field_color = 'lightgray'
    
        if self.register_first_name_field_active:
            register_first_name_field_color = 'lightblue'
        else:
            register_first_name_field_color = 'lightgray'

        if self.register_email_field_active:
            register_email_field_color = 'lightblue'
        else:
            register_email_field_color = 'lightgray'

        if self.register_phone_field_active:
            register_phone_field_color = 'lightblue'
        else:
            register_phone_field_color = 'lightgray'
    
        if self.register_username_field_active:
            register_username_field_color = 'lightblue'
        else:
            register_username_field_color = 'lightgray'

        if self.register_password_field_active:
            register_password_field_color = 'lightblue'
        else:
            register_password_field_color = 'lightgray'

        if self.register_confirm_password_field_active:
            register_confirm_password_field_color = 'lightblue'
        else:
            register_confirm_password_field_color = 'lightgray'

        # TODO seems like this can be a function
        # Label
        self.screen.blit(self.register_last_name_label, pygame.Rect(300, 50, 140, 32))
        # Field
        pygame.draw.rect(self.screen, register_last_name_field_color, self.register_last_name_input_field)
        self.register_last_name_render = self.main_font.render(self.register_last_name_input, True, "black")
        self.screen.blit(self.register_last_name_render, self.register_last_name_input_field)

        # Label
        self.screen.blit(self.register_first_name_label, pygame.Rect(500, 50, 140, 32))
        # Field
        pygame.draw.rect(self.screen, register_first_name_field_color, self.register_first_name_input_field)
        self.register_first_name_render = self.main_font.render(self.register_first_name_input, True, "black")
        self.screen.blit(self.register_first_name_render, self.register_first_name_input_field)
 
        # Label
        self.screen.blit(self.register_email_label, pygame.Rect(300, 150, 140, 32))
        # Field
        pygame.draw.rect(self.screen, register_email_field_color, self.register_email_input_field)
        self.register_email_render = self.main_font.render(self.register_email_input, True, "black")
        self.screen.blit(self.register_email_render, self.register_email_input_field)

        # Label
        self.screen.blit(self.register_phone_label, pygame.Rect(500, 150, 140, 32))
        # Field
        pygame.draw.rect(self.screen, register_phone_field_color, self.register_phone_input_field)
        self.register_phone_render = self.main_font.render(self.register_phone_input, True, "black")
        self.screen.blit(self.register_phone_render, self.register_phone_input_field)

        # Label
        self.screen.blit(self.register_username_label, pygame.Rect(300, 250, 140, 32))
        # Field
        pygame.draw.rect(self.screen, register_username_field_color, self.register_username_input_field)
        self.register_username_render = self.main_font.render(self.register_username_input, True, "black")
        self.screen.blit(self.register_username_render, self.register_username_input_field)

        # Label
        self.screen.blit(self.register_password_label, pygame.Rect(300, 350, 140, 32))
        # Field
        pygame.draw.rect(self.screen, register_password_field_color, self.register_password_input_field)
        self.register_password_render = self.main_font.render(self.register_password_input, True, "black")
        self.screen.blit(self.register_password_render, self.register_password_input_field)

        # Label
        self.screen.blit(self.register_confirm_password_label, pygame.Rect(500, 350, 140, 32))
        # Field
        pygame.draw.rect(self.screen, register_confirm_password_field_color, self.register_confirm_password_input_field)
        self.register_confirm_password_render = self.main_font.render(self.register_confirm_password_input, True, "black")
        self.screen.blit(self.register_confirm_password_render, self.register_confirm_password_input_field)

        ## Messages 
        self.register_information = self.main_font.render(self.message_text, True, "orange")
        self.screen.blit(self.register_information, pygame.Rect(200, 800, 140, 32))

        self.register_information2 = self.main_font.render(self.message_text2, True, "orange")
        self.screen.blit(self.register_information2, pygame.Rect(200, 820, 140, 32))
        # self.register_error = self.main_font.render(self.message_text, True, "red")
        # self.screen.blit(self.register_error, pygame.Rect(200, 800, 140, 32))

        ### Buttons
        self.screen.blit(self.submit_button_text, self.submit_button)
        self.screen.blit(self.cancel_button_text, self.cancel_button)

    def main(self):

        # TODO account display (+ username)
        # [TOP-LEFT]

        # TODO Either display all accounts and transfert by id to id, or select an account and display it, then transfert from it
        # Sort buttons
        self.screen.blit(self.main_sort_button_from_text, self.main_sort_button_from)
        self.screen.blit(self.main_sort_button_to_text, self.main_sort_button_to)
        self.screen.blit(self.main_sort_button_amount_text, self.main_sort_button_amount)
        self.screen.blit(self.main_sort_button_date_text, self.main_sort_button_date)
        self.screen.blit(self.main_sort_button_type_text, self.main_sort_button_type)
        self.screen.blit(self.main_sort_button_category_text, self.main_sort_button_category)
        self.screen.blit(self.main_filter_dates_button_text, self.main_filter_dates_button)
        # TODO Transaction list display
        #[BOTTOM-LEFT]

        # TODO Transaction actions (sub_state)
        #[RIGHT]

        # Quit button
        self.screen.blit(self.main_logoff_button_text, self.main_logoff_button)

    def verif_login(self):
        self.cursor.execute(f"SELECT salt FROM users WHERE username = '{self.login_username_input}';")
        try:
            salt = self.cursor.fetchall()[0][0]
            raw_password = self.pepper + self.login_password_input + salt
            password = sha256(raw_password.encode()).hexdigest()

            self.cursor.execute(f"SELECT id, username FROM users WHERE username = '{self.login_username_input}' AND password = '{password}';")
            user_data = self.cursor.fetchall()

            if bool(user_data):
                return user_data[0][0], user_data[0][1]
        except Exception:
            self.message_text = "Error in retriving user data!"
        return False

    def login_failed(self):
        self.message_text = "Login failed! Please verify if the username or password is correct"

    def create_session(self, user_data):
        self.user = Sessions.create_session(user_data)

    def create_account(self):
        """Called when clicking "submit" in register menu"""
        # TODO to simplify when refractored in loop (with a 'for'?)
        if not self.register_last_name_input or not self.register_first_name_input or not self.register_email_input or not self.register_phone_input or not self.register_username_input or not self.register_password_input or not self.register_confirm_password_input:
            self.message_text = "Please fill all the forms"
        # Check if username already exists in "users" database
        elif not self.email_is_valid():
            self.message_text = "Email not valid!"
        elif not self.phone_is_valid():
            self.message_text = "Phone not valid!"
        elif self.username_exists():
            self.message_text = "Username already exists!"
        elif self.register_password_input != self.register_confirm_password_input:
            self.message_text = "Passwords must be the same!"
        elif not self.password_is_valid():
            self.message_text = "Password must be 10 to 99 characters long, contain 1 uppercase letter,"
            self.message_text2 = "1 lowercase letter, a number and a special symbol!"
        else:  
            salt = 'b' # need to create a column for it in user
            username = self.register_username_input
            raw_password = self.pepper + self.register_password_input + salt
            password = sha256(raw_password.encode()).hexdigest()
            last_name = self.register_last_name_input
            first_name = self.register_first_name_input
            email = self.register_email_input
            phone = self.register_phone_input

            self.cursor.execute(f"INSERT INTO users (username, password, salt, last_name, first_name, email, phone) \
                                     VALUES ('{username}', '{password}', '{salt}', '{last_name}', '{first_name}', '{email}', '{phone}');")
            self.mydb.commit()
            return True
        return False

    def email_is_valid(self):
        regex_pattern = re.compile('^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$')
        return regex_pattern.match(self.register_email_input)

    def phone_is_valid(self):
        regex_pattern = re.compile('^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$')
        return regex_pattern.match(self.register_phone_input)

    def username_exists(self):
        self.cursor.execute(f"SELECT username FROM users where username = '{self.register_username_input}'")
        return self.cursor.fetchall()

    def password_is_valid(self):
        # Something like: ^ is first chara, % is last chara checked, . and * are wildcards or something, ? too I think and the = I don't know but it works (I think)        
        regex_pattern = re.compile('^(?=\S{10,99}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')

        return regex_pattern.match(self.register_password_input)

    def events(self, app_state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if app_state == "login":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.login_username_input_field.collidepoint(event.pos):
                        self.login_username_field_active = True
                        self.login_password_field_active = False
                    elif self.login_password_input_field.collidepoint(event.pos):
                        self.login_username_field_active = False 
                        self.login_password_field_active = True
                    else:
                        self.login_username_field_active = False 
                        self.login_password_field_active = False

                    if self.login_button.collidepoint(event.pos):
                        logged_user = self.verif_login()
                        if logged_user:
                            self.create_session(logged_user)
                            self.app_state = "main"
                        else:
                            self.login_failed()
                    if self.register_button.collidepoint(event.pos):
                        self.app_state = "register"

                if event.type == pygame.KEYDOWN: # TODO need to simplify this
                    if event.key == pygame.K_RETURN:
                        logged_user = self.verif_login()
                        if logged_user:
                            self.create_session(logged_user)
                            self.app_state = "main"
                        else:
                            self.login_failed()
                    elif self.login_password_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.login_password_input = self.login_password_input[:-1]
                            self.login_password_input_spoof = self.login_password_input_spoof[:-1]
                        elif event.key == pygame.K_TAB:
                            self.login_username_field_active = True
                            self.login_password_field_active = False
                        else:
                            previous_lenght = len(self.login_password_input)
                            self.login_password_input += event.unicode
                            for i in range(len(self.login_password_input) - previous_lenght):
                                self.login_password_input_spoof += "*"
                            

                    elif self.login_username_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.login_username_input = self.login_username_input[:-1]
                        elif event.key == pygame.K_TAB:
                            self.login_username_field_active = False
                            self.login_password_field_active = True
                        else:
                            self.login_username_input += event.unicode


            if app_state == "register":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # TODO Following fields refractor, refractor this too
                    if self.register_last_name_input_field.collidepoint(event.pos):
                        self.register_last_name_field_active = True
                        self.register_first_name_field_active = False
                        self.register_email_field_active = False
                        self.register_phone_field_active = False
                        self.register_username_field_active = False
                        self.register_password_field_active = False
                        self.register_confirm_password_field_active = False
                    elif self.register_first_name_input_field.collidepoint(event.pos):
                        self.register_last_name_field_active = False
                        self.register_first_name_field_active = True
                        self.register_email_field_active = False
                        self.register_phone_field_active = False
                        self.register_username_field_active = False
                        self.register_password_field_active = False
                        self.register_confirm_password_field_active = False
                    elif self.register_email_input_field.collidepoint(event.pos):
                        self.register_last_name_field_active = False
                        self.register_first_name_field_active = False
                        self.register_email_field_active = True
                        self.register_phone_field_active = False
                        self.register_username_field_active = False
                        self.register_password_field_active = False
                        self.register_confirm_password_field_active = False
                    elif self.register_phone_input_field.collidepoint(event.pos):
                        self.register_last_name_field_active = False
                        self.register_first_name_field_active = False
                        self.register_email_field_active = False
                        self.register_phone_field_active = True
                        self.register_username_field_active = False
                        self.register_password_field_active = False
                        self.register_confirm_password_field_active = False
                    elif self.register_username_input_field.collidepoint(event.pos):
                        self.register_last_name_field_active = False
                        self.register_first_name_field_active = False
                        self.register_email_field_active = False
                        self.register_phone_field_active = False
                        self.register_username_field_active = True
                        self.register_password_field_active = False
                        self.register_confirm_password_field_active = False
                    elif self.register_password_input_field.collidepoint(event.pos):
                        self.register_last_name_field_active = False
                        self.register_first_name_field_active = False
                        self.register_email_field_active = False
                        self.register_phone_field_active = False
                        self.register_username_field_active = False 
                        self.register_password_field_active = True
                        self.register_confirm_password_field_active = False
                    elif self.register_confirm_password_input_field.collidepoint(event.pos):
                        self.register_last_name_field_active = False
                        self.register_first_name_field_active = False
                        self.register_email_field_active = False
                        self.register_phone_field_active = False
                        self.register_username_field_active = False 
                        self.register_password_field_active = False
                        self.register_confirm_password_field_active = True
                    else:
                        self.register_last_name_field_active = False
                        self.register_first_name_field_active = False
                        self.register_email_field_active = False
                        self.register_phone_field_active = False
                        self.register_username_field_active = False 
                        self.register_password_field_active = False
                        self.register_confirm_password_field_active = False

                    if self.cancel_button.collidepoint(event.pos):
                        self.app_state = "login"

                    if self.submit_button.collidepoint(event.pos):
                        if self.create_account():
                            self.app_state = "login"

                if event.type == pygame.KEYDOWN: # TODO need to simplify this
                    if event.key == pygame.K_RETURN:
                        if self.create_account():
                            self.app_state = "login"
                    elif self.register_confirm_password_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_confirm_password_input = self.register_confirm_password_input[:-1]
                        elif event.key == pygame.K_TAB:
                            self.register_last_name_field_active = True
                            self.register_first_name_field_active = False
                            self.register_email_field_active = False
                            self.register_phone_field_active = False
                            self.register_username_field_active = False 
                            self.register_password_field_active = False
                            self.register_confirm_password_field_active = False
                        else:
                            self.register_confirm_password_input += event.unicode
                    elif self.register_password_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_password_input = self.register_password_input[:-1]
                        elif event.key == pygame.K_TAB:
                            self.register_last_name_field_active = False
                            self.register_first_name_field_active = False
                            self.register_email_field_active = False
                            self.register_phone_field_active = False
                            self.register_username_field_active = False 
                            self.register_password_field_active = False
                            self.register_confirm_password_field_active = True
                        else:
                            self.register_password_input += event.unicode

                    elif self.register_username_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_username_input = self.register_username_input[:-1]
                        elif event.key == pygame.K_TAB:
                            self.register_last_name_field_active = False
                            self.register_first_name_field_active = False
                            self.register_email_field_active = False
                            self.register_phone_field_active = False
                            self.register_username_field_active = False 
                            self.register_password_field_active = True
                            self.register_confirm_password_field_active = False
                        else:
                            self.register_username_input += event.unicode

                    elif self.register_phone_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_phone_input = self.register_phone_input[:-1]
                        elif event.key == pygame.K_TAB:
                            self.register_last_name_field_active = False
                            self.register_first_name_field_active = False
                            self.register_email_field_active = False
                            self.register_phone_field_active = False
                            self.register_username_field_active = True 
                            self.register_password_field_active = False
                            self.register_confirm_password_field_active = False
                        else:
                            self.register_phone_input += event.unicode

                    elif self.register_email_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_email_input = self.register_email_input[:-1]
                        elif event.key == pygame.K_TAB:
                            self.register_last_name_field_active = False
                            self.register_first_name_field_active = False
                            self.register_email_field_active = False
                            self.register_phone_field_active = True
                            self.register_username_field_active = False 
                            self.register_password_field_active = False
                            self.register_confirm_password_field_active = False
                        else:
                            self.register_email_input += event.unicode
                            
                    elif self.register_first_name_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_first_name_input = self.register_first_name_input[:-1]
                        elif event.key == pygame.K_TAB:
                            self.register_last_name_field_active = False
                            self.register_first_name_field_active = False
                            self.register_email_field_active = True
                            self.register_phone_field_active = False
                            self.register_username_field_active = False 
                            self.register_password_field_active = False
                            self.register_confirm_password_field_active = False
                        else:
                            self.register_first_name_input += event.unicode

                    elif self.register_last_name_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_last_name_input = self.register_last_name_input[:-1]
                        elif event.key == pygame.K_TAB:
                            self.register_last_name_field_active = False
                            self.register_first_name_field_active = True
                            self.register_email_field_active = False
                            self.register_phone_field_active = False
                            self.register_username_field_active = False 
                            self.register_password_field_active = False
                            self.register_confirm_password_field_active = False
                        else:
                            self.register_last_name_input += event.unicode

            if self.app_state == "main":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.main_logoff_button.collidepoint(event.pos):
                        self.app_state = "login"


# TODO Some login page
# TODO some resister page that create an user

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