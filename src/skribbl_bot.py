from typing import Optional

from google_images_search import GoogleImagesSearch
from selenium.webdriver.chrome.webdriver import WebDriver

from skribbl_room import SkribblRoom


class SkribblBot:
    def __init__(self, name: str, gis: GoogleImagesSearch):
        self.__name = name
        self.__gis = gis
        self.__room: Optional[SkribblRoom] = None

    def __join_room(self) -> None:
        room_code = input("Room code: ")
        self.__room = SkribblRoom(room_code)
        self.__room.choose_name(self.__name)

    def __create_room(self) -> None:
        self.__room = SkribblRoom()
        self.__room.choose_name(self.__name)
        url = self.__room.create()

        print(f"Use this link to join the room:\n{url}\n")

        input("Press any key to start the game...")

        self.__room.wait_game_start()

    def __get_room_action_input(self) -> None:
        is_valid_action = False
        while not is_valid_action:
            action = int(input("Choose action:\n1 - Create Room\n2 - Join Room\n\nAction number: "))
            print()  # adds a newline
            match action:
                case 1:
                    is_valid_action = True
                    self.__create_room()
                case 2:
                    is_valid_action = True
                    self.__join_room()
                case _:
                    print("\nWrong action number\n")

    def run(self):
        self.__get_room_action_input()

        while True:
            pass
