from selenium import webdriver
from selenium import webelement

# open chrome
driver = webdriver.Chrome("Player/drivers/chromedriver.exe")

# nav to wordle
print('Accessing Wordle via Chrome')
wordle_url = "https://www.nytimes.com/games/wordle/index.html"
driver.get(wordle_url)

# bust past the shadowdoms
print("Busting pass the shadowdoms...")
root1 = driver.findElement(By.xpath("//game-app"))