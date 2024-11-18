import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random

from trio._dtls import Record

# Constants To Change
RA_NAME = "RA NAME"
RA_EMAIL = "RA EMAIL"
BUILDING_NAME = "RESIDENT HALL"
CANDID_CONVO_NUMBER = 1             # The current candid conversation number NOV 22nd is number 2 for example

# Constants to not change
URL = 'https://forms.office.com/pages/responsepage.aspx?id=MHEXIi9k2UGSEXQjetVofa4mud85yvtJvGucI0p3CDJURFNVSjNBUUc5WEpMMFlRMVFZS1VPT1BVMy4u&route=shorturl'



def read_csv(file_name):
    with open(file_name, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        row_list = []
        for row in csvreader:
            name = create_name(row[2], row[1])
            room_number = row[0]
            conversation = row[3]
            date = row[4]
            keywords = [int(row[5]), int(row[6]), int(row[7])]
            new_resident = Resident(name, room_number, conversation, date, keywords)
            row_list.append(new_resident)
    return row_list

def create_name(first_name, last_name):
    return first_name + " " + last_name

def get_candid_index():
    if CANDID_CONVO_NUMBER < 1 or CANDID_CONVO_NUMBER > 4 or type(CANDID_CONVO_NUMBER) == float:
        raise ValueError("Please enter a int between 1 and 4 (inclusive)")
    return 4 + CANDID_CONVO_NUMBER


class Resident:
    '''
    This class defines what a resident is and it reads these
    values off of a csv file called Residents.csv
    '''

    def __init__(self, name, room_number_string, conversation_string, date_string, keywords):
        self.name = name
        self.room_number_string = room_number_string
        self.conversation_string = conversation_string
        self.date_string = date_string
        self.keywords = keywords


    def sample_print(self):
        print(self.name, self.room_number_string)
        print(self.conversation_string)


class CustomWebDriver:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.website = URL
        self.driver.get(self.website)
        sleep(50)

    def fill_fourm(self, resident):
        # Actually finding the values you are looking to enter
        questions = self.driver.find_elements(By.TAG_NAME, 'input')
        text_areas = self.driver.find_elements(By.TAG_NAME, 'textarea')
        submit_button = self.driver.find_element(By.CSS_SELECTOR, '[data-automation-id="submitButton"]')

        questions[0].send_keys(RA_NAME)
        questions[1].send_keys(RA_EMAIL)
        questions[2].send_keys(BUILDING_NAME)

        questions[3].send_keys(resident.name)
        questions[4].send_keys(resident.room_number_string)

        questions[get_candid_index()].click()

        questions[11].send_keys(resident.date_string)

        for value in resident.keywords:
            if value > 10 or value < 0:
                questions[12].click()
            else:
                questions[12 + value].click()

        text_areas[0].send_keys(resident.conversation_string)
        sleep(1)
        text_areas[1].send_keys('None')

        submit_button.click()
        sleep(3)
        self.driver.refresh()
        sleep(5)


    def close_driver(self):
        self.driver.quit()


if __name__ == '__main__':
    resident_list = read_csv('Residents.csv')
    driver = CustomWebDriver()
    for resident in resident_list:
        driver.fill_fourm(resident)
    driver.close_driver()





