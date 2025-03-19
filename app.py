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
        self.screen_size = (1200, 900)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.main_font = pygame.font.Font(None, 36)
        pygame.display.set_caption("Budget Buddy")

        # Variables outside of loop
        self.running = True
        self.app_state = "login"
        # app_substate = "a"
        self.pepper = 'a' # stocked here, doesn't change

        # Display: Login page (input fields + buttons) 
        self.login_username_input_field = pygame.Rect(300, 100, 140, 32)
        self.login_username_field_active = False
        self.login_username_input = 'a'

        self.login_password_input_field = pygame.Rect(300, 200, 140, 32)
        self.login_password_field_active = False
        self.login_password_input = 'a'

        # Buttons
        self.login_button = pygame.Rect(self.screen_size[0]*0.5, self.screen_size[1]-50, 200, 50)
        self.login_button_text = self.main_font.render("Login", True, (0, 0, 0))

        self.register_button = pygame.Rect(self.screen_size[0]*0.25, self.screen_size[1]-50, 200, 50)
        self.register_button_text = self.main_font.render("Register", True, (0, 0, 0))

        # Display: Register page (input fields + buttons)
        # TODO refractor this in a loop
        self.register_last_name_input_field = pygame.Rect(300, 100, 140, 32)
        self.register_last_name_field_active = False
        self.register_last_name_input = ''

        self.register_first_name_input_field = pygame.Rect(500, 100, 140, 32)
        self.register_first_name_field_active = False
        self.register_first_name_input = ''

        self.register_email_input_field = pygame.Rect(300, 200, 140, 32)
        self.register_email_field_active = False
        self.register_email_input = ''

        self.register_phone_input_field = pygame.Rect(500, 200, 140, 32)
        self.register_phone_field_active = False
        self.register_phone_input = ''

        # Login related
        self.register_username_input_field = pygame.Rect(300, 300, 140, 32)
        self.register_username_field_active = False
        self.register_username_input = 'a'

        self.register_password_input_field = pygame.Rect(300, 400, 140, 32)
        self.register_password_field_active = False
        self.register_password_input = 'a'

        self.register_confirm_password_input_field = pygame.Rect(500, 400, 140, 32)
        self.register_confirm_password_field_active = False
        self.register_confirm_password_input = ''

        # Buttons
        self.submit_button = pygame.Rect(self.screen_size[0]*0.5, self.screen_size[1]-50, 200, 50)
        self.submit_button_text = self.main_font.render("Submit", True, (0, 0, 0))

        self.cancel_button = pygame.Rect(self.screen_size[0]*0.25, self.screen_size[1]-50, 200, 50)
        self.cancel_button_text = self.main_font.render("Cancel", True, (0, 0, 0))

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

        pygame.draw.rect(self.screen, login_username_field_color, self.login_username_input_field)
        self.login_username_render = self.main_font.render(self.login_username_input, True, "black")
        self.screen.blit(self.login_username_render,self.login_username_input_field)

        pygame.draw.rect(self.screen, login_password_field_color, self.login_password_input_field)
        self.login_password_render = self.main_font.render(self.login_password_input, True, "black")
        self.screen.blit(self.login_password_render,self.login_password_input_field)

        # Buttons
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
        pygame.draw.rect(self.screen, register_last_name_field_color, self.register_last_name_input_field)
        self.register_last_name_render = self.main_font.render(self.register_last_name_input, True, "black")
        self.screen.blit(self.register_last_name_render, self.register_last_name_input_field)

        pygame.draw.rect(self.screen, register_first_name_field_color, self.register_first_name_input_field)
        self.register_first_name_render = self.main_font.render(self.register_first_name_input, True, "black")
        self.screen.blit(self.register_first_name_render, self.register_first_name_input_field)

        pygame.draw.rect(self.screen, register_email_field_color, self.register_email_input_field)
        self.register_email_render = self.main_font.render(self.register_email_input, True, "black")
        self.screen.blit(self.register_email_render, self.register_email_input_field)

        pygame.draw.rect(self.screen, register_phone_field_color, self.register_phone_input_field)
        self.register_phone_render = self.main_font.render(self.register_phone_input, True, "black")
        self.screen.blit(self.register_phone_render, self.register_phone_input_field)

        pygame.draw.rect(self.screen, register_username_field_color, self.register_username_input_field)
        self.register_username_render = self.main_font.render(self.register_username_input, True, "black")
        self.screen.blit(self.register_username_render, self.register_username_input_field)

        pygame.draw.rect(self.screen, register_password_field_color, self.register_password_input_field)
        self.register_password_render = self.main_font.render(self.register_password_input, True, "black")
        self.screen.blit(self.register_password_render, self.register_password_input_field)

        pygame.draw.rect(self.screen, register_confirm_password_field_color, self.register_confirm_password_input_field)
        self.register_confirm_password_render = self.main_font.render(self.register_confirm_password_input, True, "black")
        self.screen.blit(self.register_confirm_password_render, self.register_confirm_password_input_field)

        # Buttons
        self.screen.blit(self.submit_button_text, self.submit_button)
        self.screen.blit(self.cancel_button_text, self.cancel_button)

    def main(self):
        pass

    def verif_login(self):
        self.cursor.execute(f"SELECT salt FROM users WHERE username = '{self.login_username_input}';")
        salt = self.cursor.fetchall()[0][0]

        raw_password = self.pepper + self.register_password_input + salt
        password = sha256(raw_password.encode()).hexdigest()
        
        self.cursor.execute(f"SELECT id, username FROM users WHERE username = '{self.login_username_input}' AND password = '{password}';")
        user_data = self.cursor.fetchall()

        if bool(self.cursor.fetchall()):
            return user_data[0][0], user_data[0][1]
        return False

    def login_failed(self):
        pass

    def create_account(self):
        """Called when clicking "submit" in register menu"""
        if not self.register_last_name_input or not self.register_first_name_input or not self.register_email_input or not self.register_phone_input or not self.register_username_input or not self.register_password_input or not self.register_confirm_password_input:
            print("Please fill all the forms")
        # Check if username already exists in "users" database
        elif self.username_exists():
            print("Username already exists!")
        elif self.register_password_input != self.register_confirm_password_input:
            print("Passwords must be the same!")
        else:  
            # Check if password is valid (6-20 chara, 1 upper and 1 lower case, 1 number and 1 special chara)
            if self.password_is_valid():
                salt = 'b' # need to create a column for it in user
                username = self.register_username_input
                raw_password = self.pepper + self.register_password_input + salt
                password = sha256(raw_password.encode()).hexdigest()
                last_name = self.register_last_name_input
                first_name = self.register_first_name_input
                email = self.register_email_input
                phone = self.register_phone_input

                self.cursor.execute(f"INSERT INTO users (username, password, salt, last_name, first_name, email, phone) \
                                     VALUES ('{username}', '{password}', '{salt}', '{last_name}', '{first_name}', '{email}', '{phone}'")
                self.mydb.commit()
                return True
            else:
                print("Password must be 6 to 20 character long, contain 1 uppercase letter, 1 lowercase latter, a number and a special symbol!") 
        return False

    def username_exists(self):
        self.cursor.execute(f"SELECT username FROM users where username = '{self.register_username_input}'")
        return self.cursor.fetchall()

    def password_is_valid(self):
        # Something like: ^ is first chara, % is last chara checked, . and * are wildcards or something, ? too I think and the = I don't know but it works (I think)        
        regex_pattern = re.compile('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')

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
                            self.login_failed() # TODO
                    if self.register_button.collidepoint(event.pos):
                        self.app_state = "register"

                if event.type == pygame.KEYDOWN: # TODO need to simplify this
                    if self.login_username_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.login_username_input = self.login_username_input[:-1]
                        else:
                            self.login_username_input += event.unicode
                    if self.login_password_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.login_password_input = self.login_password_input[:-1]
                        else:
                            self.login_password_input += event.unicode

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
                    if self.register_confirm_password_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_confirm_password_input = self.register_confirm_password_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            if self.create_account():
                                self.app_state = "login"
                        elif event.key == pygame.K_TAB:
                            pass
                        else:
                            self.register_confirm_password_input += event.unicode
                    if self.register_password_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_password_input = self.register_password_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            pass
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

                    if self.register_username_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_username_input = self.register_username_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            pass
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

                    if self.register_phone_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_phone_input = self.register_phone_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            pass
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

                    if self.register_email_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_email_input = self.register_email_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            pass
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
                            
                    if self.register_first_name_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_first_name_input = self.register_first_name_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            pass
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

                    if self.register_last_name_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.register_last_name_input = self.register_last_name_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            pass
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

# TODO Some login page
# TODO some resister page that create an user

# --- Test ---
# --- ---- ---

#for creating an account (user can have several)
#this goes in a "create an bank account" button
                # try:
                #     self.user.account_creation(cursor, mydb)
                # except Exception:
                #     print("Error in account creation")


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