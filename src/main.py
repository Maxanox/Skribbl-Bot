from google_images_search import GoogleImagesSearch
from selenium import webdriver

from skribbl_bot import SkribblBot

KEY = "AIzaSyCaNmJqnUZVUqDfaJ42AXz9-0Z78CD24sE"
CX = "52e363b86b1c2467f"


def main():
    gis = GoogleImagesSearch(KEY, CX)

    name = input("Your bot name: ")

    skribbl_bot = SkribblBot(name, gis)
    skribbl_bot.run()


if __name__ == "__main__":
    main()
