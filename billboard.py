from selenium import webdriver  # First : pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from multiprocessing import Pool
from selenium.webdriver.common.keys import Keys
import datetime
from time import sleep
from random import randint
from os import name
import sys
import datetime
import json 

OS = name  # os.name: Windows return 'nt', Linux and MacOS return 'posix'

BUILDING_LIST_TEST = { "HALL" : "5f6c001ba708af000a5e2487", "ateliers-a":"5f7a06d3610280000a8485fd" }
BUILDING_LIST_TEST.get("HALL")

BUILDING_LIST = []

EVENTS_FILE_TEST = 'programme.json' #'guests_list_0.txt' #for 401 guests: 'guests.txt'
EVENTS_FILE = ""

BUILDING_LIST = []
start_time = datetime.datetime.now()


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

    def edit_billboard(self, eventId):
        self.driver.get(f'{self.base_url}/event/floor-plan/{eventId}')

        #right billboard button
        WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div[5]/ul/li[2]"))).click()

        sleep(1)    

        #select textarea and text inside
        WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div[5]/ul/div[2]/div/div/div[2]/div/div/textarea'))).send_keys(Keys.CONTROL + "a")
        sleep(1)  

        #select textarea and update it
        WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div/div[5]/ul/div[2]/div/div/div[2]/div/div/textarea'))).send_keys("POUET")
        sleep(1)
        #apply
        WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[2]/button[2]"))).click()
        sleep(1)
        #summary
        WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[2]/button[2]"))).click()
        #save
        sleep(1)
        WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[2]/button[2]"))).click()
        #WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH, ''))).click()
        sleep(5)

def build_agenda_per_day():
    # Opening JSON file 
    f = open('programme.json',) 
    
    # returns JSON object as  
    # a dictionary 
    data = json.load(f) 
    
    sorted_list = sorted(data, key=lambda k: (k['date'],k["location"],k["timeStart"]))

    text =""
    for event in sorted_list:
        if event.get('date') == datetime.date.today():
            print('TODAY')
        else:
            text = text + event.get('timeStart')+":"+event.get('timeStart')+" " + event.get('title') + "\n " 
        # elif event.get('date') == '2020-11-17' :
        #     print('not TODAY')
        # elif event.get('date') == '2020-11-18' :
        #     print('2020-11-18')
        # elif event.get('date') == '2020-11-19' :
        #     print('2020-11-19')
        # elif event.get('date') == '2020-11-20' :
        #     print('2020-11-20')
        # elif event.get('date') == '2020-11-21' :
        #     print('2020-11-21')
        print(text)
        if event.get("location") == 'ateliers-a':
            print(event.get("title"))
    # Iterating through the json 
    # list 
    # print(sorted_list)
    # for i in data: 
    #     print(i) 
    
    # Closing file 
    f.close() 

build_agenda_per_day()

exit()


BUILDING_LIST = BUILDING_LIST_TEST

remo_bot = remoBot('lefrancois.c@avados.net', 'e4ZKj7CmfVZPD7T\'Wx"u')
remo_bot.edit_billboard(BUILDING_LIST["HALL"])

end_time = datetime.datetime.now()
print("Total time" + str( end_time -start_time ))
