from enum import Enum

from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class RoomState(Enum):
    Draw = "Draw"
    Guess = "Guess"
    Waiting = "Waiting"


class SkribblRoom:
    BASE_URL = "https://skribbl.io/"

    BUTTON_COOKIE_SKIP_SELECTOR = ".cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes"
    BUTTON_CREATE_ROOM_CLASS = "button-create"
    BUTTON_START_ID = "start-game"
    BUTTON_START_RANDOM_CLASS = "button-play"

    INPUT_NAME_CLASS = "input-name"
    INPUT_INVITE_LINK_ID = "input-invite"
    
    DIV_CHAT_CONTENT_CLASS = "chat-content"

    def __init__(self, room_code: Optional[str] = None):
        self.__driver = webdriver.Chrome()
        self.__driver.get(self.BASE_URL + '?' + room_code if room_code else self.BASE_URL)

        self.__state = RoomState.Waiting

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
                text = children_p_e[-1].text

            try:
                button_e = self.__driver.find_element(By.ID, self.BUTTON_START_ID)
            except NoSuchElementException as e:
                raise Exception(f"Start button not found:\n{e.msg}")
            else:
                button_e.click()

    def start_random_game(self):
        try:
            button_e = self.__driver.find_element(By.CLASS_NAME, self.BUTTON_START_RANDOM_CLASS)
        except NoSuchElementException as e:
            raise Exception(f"Start random game button not found:\n{e.msg}")
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
