from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumbase import BaseCase

class PlayWordle(BaseCase):
    def test(self):
        self.open("https://www.nytimes.com/games/wordle/index.html")
        self.click("game-app::shadow game-modal::shadow game-icon")
        keyboard_base = "game-app::shadow game-keyboard::shadow "