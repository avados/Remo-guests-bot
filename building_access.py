from selenium import webdriver  # First : pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from multiprocessing import Pool

from time import sleep
from random import randint
from os import name
import sys
import datetime
import config as cfg


OS = name  # os.name: Windows return 'nt', Linux and MacOS return 'posix'



GUEST_LIST_200 = []





start_time = datetime.datetime.now()

def get_splitted_guest_list_200(guestList):
    """
        remo can only take emails 200 at a time, so we split the list by 200
    """
    _guests = []
    _splited_guests = []

    with open(guestList, 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                _guests.append(line) 
            f.close()
    
    

    while(len(_guests) > 199):
        _splited_guests.append(_guests[0:199])
        del _guests[0:199]
    
    _splited_guests.append(_guests)
    


    return _splited_guests


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



        if OS == 'nt': 
            # op = webdriver.ChromeOptions()
            # op.add_argument('headless')
            # self.driver = webdriver.Chrome('chromedriver.exe',options=op)
            self.driver = webdriver.Chrome('chromedriver.exe')
        else: 
            self.driver = webdriver.Chrome()
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

    def add_guests(self, eventId, guestLists):
        """
            Make the program fill guests emails on Remo

            Args:
                self: make the fonction able to get the class variables.
                eventId: used to select the event on which guests should be invited
                guestList: the list of guests to invite
        """
        local_start_time = datetime.datetime.now()
        self.driver.get(f'{self.base_url}/event/guests/{eventId}')

        # Code to open, read and use the guests file
        # with open(guestList, 'r') as f:
        #     lines = f.read().splitlines()
        #     for line in lines:
        #         self.guests.append(line)
        #     f.close()

        # Code to write the guests email adresses on Remo
        enter_guest_email = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div/input')))
        
        # enter_guest_email.send_keys(guestList[0]+ '\n')
        for guestList in guestLists:
            for guest in guestList:
                enter_guest_email.send_keys(guest + '\n')
            sleep(1)
            # Click "add to guests list" button
            self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div[1]/div[3]/button').click()
            #/html/body/div[4]/div[3]/div/div[2]/button[2]
            sleep(1)
            
            #we can have a different path on load, if there is nothing in remo's guest list
            try:
                WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/button[2]'))).click()
            except TimeoutException as to:
                WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div/div[2]/button[2]'))).click()
            
            sleep(1)

        local_end_time = datetime.datetime.now()
        print("add guest time" + str(local_end_time -local_start_time ))

        
        

    def remove_guests(self, eventId, removeLists):
        """
            Make the program remove guest(s) email(s) on Remo

            Args:
                self: make the fonction able to get the class variables.
                eventId: used to select the event from which guest(s) should be removed
                guestList: the list of guests to remove
        """
        self.driver.get(f'{self.base_url}/event/guests/{eventId}')
        local_start_time = datetime.datetime.now()

        # Code to open, read and use the guests file
        remove_guest = []
        # with open(removeList, 'r') as f:
        #     lines = f.read().splitlines()
        #     for line in lines:
        #         remove_guest.append(line)
        #     f.close()

        # Code to write the guests email adresses on Remo
        for remove_guest in removeLists:
            for guest in remove_guest:
                
                #write name in search field
                try:
                    
                    WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div[3]/div/div[1]/div[1]/div[2]/div/input'))).send_keys(guest)
                except TimeoutException as identifier:
                    WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div/div[2]/div/div[1]/div/div/input'))).send_keys(guest)

                # If guest is removable : removed - else blocked
                sleep(1)
                try:
                    #confirm delete
                    WebDriverWait(self.driver, 1).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div[3]/div/div[2]/div/div/div/table/tbody/tr[1]/td[1]/div/button[3]'))).click()
                    sleep(1)
                    WebDriverWait(self.driver, 1).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div/div[2]/button[1]'))).click()
                    sleep(1)
                except :
                    #clear field
                    sleep(2)
                    WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div[3]/div/div[1]/div[1]/div[2]/div/div[2]/button' ))).click()
                    #clear is not working as there is a button to empty the fieldWebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div[3]/div/div[1]/div[1]/div[2]/div/input'))).clear()
                    print("Guest " + guest + " not found")
                    sleep(1)

        local_end_time = datetime.datetime.now()
        print("remove guest time" + str(local_end_time -local_start_time ))
            
                

    def edit_event(self):
        """ 
            not usefull anymore, can navigate directly from the URL
        """
        WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/button'))).click()

        #elem = self.driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div[11]/div/a/div/div[4]/div[2]/div/a[3]")
        elem = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div[11]/div/a/div/div[4]/div[2]/div/a[3]")
        actions = ActionChains(self.driver)
        actions.move_to_element(elem).perform()
        sleep(5)
        WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div[11]/div/a/div/div[4]/div[2]/div/a[3]"))).click()
        


MODE = "TEST"
#if __name__ == '__main__':
"""
    This condition ensures that the program only works if this file is the one that the user has launched.
"""
    

# script name is always the first arg
# if (len(sys.argv) != 3) :
#     print("Error: Not enough args provided")
#     print("Usage: python main.py  MODE ACTION")
#     print("mode available: PROD; TEST")
#     print("Action available: DEL; ADD" )
#     exit()



GUEST_FILE = ""
MODE = sys.argv[3]
BUILDING_LIST=[]
if  MODE == "TEST" :
    print('Test mode')
    GUEST_FILE = cfg.GUEST_FILE_TEST
    BUILDING_LIST = cfg.BUILDING_LIST_TEST
elif MODE == "PROD" :
    print('Prod mode')
    GUEST_FILE = cfg.GUEST_FILE_PROD
    BUILDING_LIST = cfg.BUILDING_LIST_PROD
else:
    MODE = "TEST"
    GUEST_FILE = cfg.GUEST_FILE_TEST
    BUILDING_LIST = cfg.BUILDING_LIST_TEST

# if  "TEST" in sys.argv:
#     print('Test mode')
#     MODE = "TEST"
#     GUEST_FILE = cfg.GUEST_FILE_TEST
#     BUILDING_LIST = cfg.BUILDING_LIST_TEST
# elif "PROD" in sys.argv:
#     print('Prod mode')
#     MODE = "PROD"
#     GUEST_FILE = cfg.GUEST_FILE_PROD
#     BUILDING_LIST = cfg.BUILDING_LIST_PROD
# else:
#     MODE = "TEST"
#     GUEST_FILE = cfg.GUEST_FILE_TEST
#     BUILDING_LIST = cfg.BUILDING_LIST_TEST

GUEST_LIST_200 = get_splitted_guest_list_200( GUEST_FILE )




ROOM = sys.argv[1]

remo_bot = remoBot(cfg.REMO_LOGIN, cfg.REMO_PASSWORD)

if "DEL" in sys.argv:
    print('Action Del') 
    remo_bot.remove_guests( BUILDING_LIST[ROOM], GUEST_LIST_200)
elif "ADD" in sys.argv:
    print('Action add') 
    remo_bot.add_guests( BUILDING_LIST[ROOM], GUEST_LIST_200)

##remo_bot.driver.close()

sleep(5)

end_time = datetime.datetime.now()
print("Total time" + str( end_time -start_time ))
