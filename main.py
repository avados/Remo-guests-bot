from selenium import webdriver  # First : pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep
from random import randint
from os import name

OS = name  # os.name: Windows return 'nt', Linux and MacOS return 'posix'
print(OS)

class remoBot:
    def __init__(self, username, password):
        """
            Initializes an instance of the Remo bot class.

            Args:
                username: use the username provided when the class is initializated.
                password: use the password provided when the class is initializated.

            Variables:
                * self: make the variable available in the class instead of into a single function.
                base_url: the website base url where the bot should work.
                random_string: a random string to fill the company name and/or event name.
                OS: Make the program able to run on MacOS, Linux and Windows by changing the command depending on the current OS
        """
        self.username = username
        self.password = password
        self.base_url = 'https://live.remo.co'
        self.guests = []

        self.random_string = ''
        for _ in range (randint(12, 24)): self.random_string += 'abcdefghijklmnopqrstuvwxyz'[randint(0, 25)]

        if OS == 'nt': self.driver = webdriver.Chrome('chromedriver.exe')
        else: self.driver = webdriver.Chrome()
        self.login()

    def login(self):
        """
            Logs a user into Remo via the web portal.

            Args:
                self: make the fonction able to get the class variables.

            Variables:
                enter_username: the variable used to fill the username with the provided one when the class was initalizated.
                enter_password: the variable used to fill the password with the provided one when the class was initalizated.
        """
        self.driver.get(f'{self.base_url}/signin')

        # Fill username and password
        enter_username = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.NAME, 'email')))
        enter_username.send_keys(self.username)
        enter_password = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.NAME, 'password')))
        enter_password.send_keys(self.password)

        # Press the Log In Button
        self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div/div/div[2]/div/form/div/div[2]/button').click()

        # Wait for the page to load (5 seconds)
        sleep(5)

    def create_company(self):
        """
            Create a company with a random name.

            Args:
                self: make the fonction able to get the class variables.
        """
        self.driver.get(f'{self.base_url}/company-register')

        # Fill the company name
        enter_random_string = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.NAME, 'companyName')))
        enter_random_string.send_keys(self.random_string)

        # Press "Save and Continue"
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div[2]/div/div[2]/div[2]/div[2]/div/button').click()

        # Wait for the page to load (5 seconds)
        sleep(5)

    def create_event(self):
        """
            Create an event with a random name.

            Args:
                self: make the fonction able to get the class variables.
        """
        self.driver.get(f'{self.base_url}/event')

        enter_event_name = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.NAME, 'eventName')))
        enter_event_name.send_keys(self.random_string)

        # self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div[2]/div/div/div[1]/div/div[1]/div[1]/label[2]/span[1]').click()

    def add_guests(self, eventId, guestList):
        """
            Make the program fill guests emails on Remo

            Args:
                self: make the fonction able to get the class variables.
                eventId: used to select the event on which guests should be invited
                guestList: the list of guests to invite
        """
        self.driver.get(f'{self.base_url}/event/guests/{eventId}')

        # Code to open, read and use the guests file
        with open(guestList, 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                self.guests.append(line)
            f.close()

        # Code to write the guests email adresses on Remo
        enter_guest_email = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div/input')))
        for guest in self.guests:
            enter_guest_email.send_keys(guest + '\n')

        # Click "add to guests list" button
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div[1]/div[3]/button').click()
        self.driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[2]/button[2]').click()
        

    def remove_guests(self, eventId, removeList):
        """
            Make the program remove guest(s) email(s) on Remo

            Args:
                self: make the fonction able to get the class variables.
                eventId: used to select the event from which guest(s) should be removed
                guestList: the list of guests to remove
        """
        self.driver.get(f'{self.base_url}/event/guests/{eventId}')

        # Code to open, read and use the guests file
        remove_guest = []
        with open(removeList, 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                remove_guest.append(line)
            f.close()

        # Code to write the guests email adresses on Remo
        for guest in remove_guest:
            WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div[3]/div/div[1]/div[1]/div[2]/div/input'))).send_keys(guest)
            # If guest is removable : removed - else blocked
            WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div[3]/div/div[2]/div/div/div/table/tbody/tr[1]/td[7]/div/button[3]'))).click()
            WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div/div[2]/button[1]'))).click()
            sleep(1)


if __name__ == '__main__':
    """
        This condition ensures that the program only works if this file is the one that the user has launched.
    """
    remo_bot = remoBot('vianney@veremme.org', 'a*4irJ5cS%9BFg6&Cy6X1u@Yn6S%5mv04KTg1MUuuSjTJxbFsn')
    remo_bot.add_guests('5f2afcc0716baa0007010a6e', 'guests_list_0.txt')
    sleep(3)
    remo_bot.remove_guests('5f2afcc0716baa0007010a6e', 'remove_guests.txt')
