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

        # Input fields
        self.login_username_input_field = pygame.Rect(300, 100, 140, 32)
        self.login_username_field_active = False
        self.login_username_input = ''
        self.login_username_render = self.main_font.render(self.login_username_input, True, "black")

        self.login_password_input_field = pygame.Rect(300, 200, 140, 32)
        self.login_password_field_active = False
        self.login_password_input = ''
        self.login_password_render = self.main_font.render(self.login_password_input, True, "black")
        

        self.login_button = pygame.Rect(self.screen_size[0]*0.5, self.screen_size[1]-50, 200, 50)
        self.login_button_text = self.main_font.render("Login", True, (0, 0, 0))

        self.register_button = pygame.Rect(self.screen_size[0]*0.25, self.screen_size[1]-50, 200, 50)
        self.register_button_text = self.main_font.render("Register", True, (0, 0, 0))

        # Register fields
        self.register_username_input_field = pygame.Rect(300, 100, 140, 32)
        self.register_username_field_active = False
        self.register_username_input = 'a'
        self.register_username_render = self.main_font.render(self.register_username_input, True, "black")

        self.register_password_input_field = pygame.Rect(300, 200, 140, 32)
        self.register_password_field_active = False
        self.register_password_input = 'a'
        self.register_password_render = self.main_font.render(self.register_password_input, True, "black")

        self.register_confirm_password_input = ''
        self.register_confirm_password_field_active = False

        self.confirm_register_button = pygame.Rect(self.screen_size[0]*0.5, self.screen_size[1]-50, 200, 50)
        self.confirm_register_button_text = self.main_font.render("Register", True, (0, 0, 0))

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
        self.screen.blit(self.login_username_render,self.login_username_input_field)
        self.screen.blit(self.login_password_render,self.login_password_input_field)

        # Buttons
        self.screen.blit(self.login_button_text, self.login_button)
        self.screen.blit(self.register_button_text, self.register_button)

    def register(self):
        self.screen.blit(self.confirm_register_button_text, self.confirm_register_button)
        self.screen.blit(self.cancel_button_text, self.cancel_button)

    def main(self):
        pass

    def verif_login(self):
        self.cursor.execute(f"SELECT id, username, password FROM users WHERE username = '{self.login_username_input}' AND password = '{sha256(self.login_password_input.encode()).hexdigest()}';")
        user_data = self.cursor.fetchall()
        if bool(self.cursor.fetchall()):
            return user_data[0][0], user_data[0][1]
        return False

    def login_failed(self):
        pass

    def create_account(self):
        # Something like: ^ is first chara, % is last chara checked, . and * are wildcards or something, ? too I think and the = I don't know but it works (I think)
        
        # Check if username already exists
        if self.username_is_valid():        
            # Check if password is valid
            if self.password_is_valid():
                pepper = 'a' # stocked here, doesn't change
                salt = 'b' # need to create a column for it in user
                username = self.register_username_input
                password = sha256(pepper + self.register_password_input.encode() + salt).hexdigest()

                
            else:
                print("Password must be 6 to 20 character long, contain 1 uppercase letter, 1 lowercase latter, a number and a special symbol!")
        else:
            print("Username already exists!")


    def username_is_valid(self):
        return self.cursor.execute(f"SELECT username FROM users where username = {self.register_username_input}")

    def password_is_valid(self):
        regex_pattern = re.compile('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')

        return regex_pattern.match(self.register_password_input)

    def create_session(self, user_data):
        # Put the id of the user here for the session (should be overwritten when new session is created)
        # This is for select requests
        user = Sessions(user_data[0], user_data[1])
        return user

    def events(self, app_state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if app_state == "login":
                if event.type == pygame.KEYDOWN: # TODO need to simplify this
                    if self.login_username_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.login_username_input = self.login_username_input[:-1]
                        else:
                            self.login_username_input += event.unicode
                    if self.login_password_field_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.login_username_input = self.login_username_input[:-1]
                        else:
                            self.login_username_input += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.login_username_input_field.collidepoint(event.pos):
                        self.login_username_field_active = True
                    elif self.login_password_input_field.collidepoint(event.pos):
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

            if app_state == "register":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.cancel_button.collidepoint(event.pos):
                        self.app_state = "login"
                    if self.cancel_button.collidepoint(event.pos):
                        self.create_account()
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