from enum import Enum

import time
from typing import Optional

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class RoomState(Enum):
    Draw = "DRAW"
    Guess = "GUESS"
    Waiting = "WAITING"
    Home = ""


class SkribblRoom:

    # The base URL of the Skribbl.io website
    BASE_URL = "https://skribbl.io/"

    # The CSS selector of the button to skip the cookies popup
    BUTTON_COOKIE_SKIP_SELECTOR = ".cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes"
    # The Class name of the button to create a room
    BUTTON_CREATE_ROOM_CLASS = "button-create"
    # The ID of the button to start the game
    BUTTON_START_ID = "start-game"
    # The Class name of the button to ready up
    BUTTON_READY_CLASS = "button-play"

    # The Class name of the input to choose a name
    INPUT_NAME_CLASS = "input-name"
    # The ID of the input to get the invite link
    INPUT_INVITE_LINK_ID = "input-invite"
    
    # The Class name of the chat content div
    DIV_CHAT_CONTENT_CLASS = "chat-content"
    # The ID of the div to get the room state
    DIV_STATE_ID = "game-word"

    def __init__(self, room_code: Optional[str] = None):
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")

        self.__driver = webdriver.Chrome(options=chrome_options)
        self.__driver.get(self.BASE_URL + '?' + room_code if room_code else self.BASE_URL)

        self.__skip_cookies_popup()

    def __skip_cookies_popup(self):
        try:
            button_e = self.__driver.find_element(By.CSS_SELECTOR, self.BUTTON_COOKIE_SKIP_SELECTOR)
        except NoSuchElementException as e:
            raise Exception(f"Cookies popup skip button not found:\n{e.msg}")
        else:
            button_e.click()

    def wait_game_start_request(self):
        try:
            div_e = self.__driver.find_element(By.CLASS_NAME, self.DIV_CHAT_CONTENT_CLASS)
        except NoSuchElementException as e:
            raise Exception(f"Chat content not found:\n{e.msg}")
        else:
            text = ""
            while text != "start":
                children_p_e = div_e.find_elements(By.TAG_NAME, 'p')
                text = children_p_e[-1].find_element(By.TAG_NAME, 'span').text

            try:
                button_e = self.__driver.find_element(By.ID, self.BUTTON_START_ID)
            except NoSuchElementException as e:
                raise Exception(f"Start button not found:\n{e.msg}")
            else:
                button_e.click()
    
    def ready(self):
        try:
            button_e = self.__driver.find_element(By.CLASS_NAME, self.BUTTON_READY_CLASS)
        except NoSuchElementException as e:
            raise Exception(f"Ready button not found:\n{e.msg}")
        else:
            button_e.click()

    def choose_name(self, name: str) -> None:
        try:
            input_e = self.__driver.find_element(By.CLASS_NAME, self.INPUT_NAME_CLASS)
        except NoSuchElementException as e:
            raise Exception(f"Name input not found:\n{e.msg}")
        else:
            input_e.send_keys(name)

    def create(self) -> str:
        try:
            button_e = self.__driver.find_element(By.CLASS_NAME, self.BUTTON_CREATE_ROOM_CLASS)
        except NoSuchElementException as e:
            raise Exception(f"Create room button not found:\n{e.msg}")
        else:
            button_e.click()

        try:
            invite_link_input_e = self.__driver.find_element(By.ID, self.INPUT_INVITE_LINK_ID)
        except NoSuchElementException as e:
            raise Exception(f"Invite link input not found:\n{e.msg}")
        else:
            invite_link = ""
            # While loop to wait the dynamic input set from the page
            while not invite_link:
                invite_link = invite_link_input_e.get_attribute('value')
                invite_link.strip()

        return invite_link

    def get_room_state(self):
        try:
            div_e = self.__driver.find_element(By.ID, self.DIV_STATE_ID)
        except NoSuchElementException as e:
            raise Exception(f"Room state div not found:\n{e.msg}")
        else:
            return RoomState(div_e.text.split(' ')[0])

    def get_word(self) -> str:
        try:
            div_e = self.__driver.find_element(By.ID, self.DIV_STATE_ID).find_element(By.CLASS_NAME, 'word')
        except NoSuchElementException as e:
            raise Exception(f"Room word div not found:\n{e.msg}")
        else:
            return div_e.text