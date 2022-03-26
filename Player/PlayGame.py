from selenium import webdriver

#helper function to get children of shadowdoms
def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root

# open chrome
driver = webdriver.Chrome("Player/drivers/chromedriver.exe")

# nav to wordle
print('Accessing Wordle via Chrome')
wordle_url = "https://www.nytimes.com/games/wordle/index.html"
driver.get(wordle_url)

# bust past the shadowdoms
print("Busting pass the shadowdoms...")

game_app = driver.find_element_by_xpath("//game-app")
shadow_root_game_app = expand_shadow_element(game_app)




driver.close()
print("Finished!")