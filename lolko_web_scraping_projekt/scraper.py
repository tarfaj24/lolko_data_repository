from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import json
import time



#david idem to po anglicky pisat lebo si chcem precvicit anglictinu a mohli to aj ostatni citat

#if you run into a click interception error its because of adds popping up and i dont have time to deal with this xd so just restart the program and hope it works

#configuration for chrome browser

#i mostly use the XPATH to find the elements i need because a lot of elements have classes that dont identify the element but are just used as CSS frameworks so the identification of elements is in the form of XPATH
 

chrome_options = Options() #You can configure the options through this command
# chrome_options.add_argument("--headless")  #closes or opens the visibility of chrome windows 
# chrome_options.add_argument("--disable-gpu") #no gpu load on your computer
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.265 Safari/537.36"
) #hides the bot as a normal user

#setup chrome webdriveru
service = Service(ChromeDriverManager().install()) #installing the chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options) #final touch of setting up the driver

url = input("URL for your account on ugg website: ")
driver.get(url)


#waits till the elements are loaded uses the driver and a 30 second max wait time

WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "pw-oop-flex_container"))
    )


#finds the accept button and clicks it so the web page can be accessed
accept_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@class="fc-button fc-cta-consent fc-primary-button"]'))
)
accept_button.click()

#finds the name of the account owner
acc_name = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//span[contains(@class,'truncate')][parent::div[contains(@class,'max-xs:text-[20px]')][parent::div[contains(@class,'mb-[8px]')]]]")))

#a scroll "function" that scrolls the elements so they can load in the DOM and be acessed as information and be clickable
scroll_count = 0
scroll = True
while scroll:
    driver.execute_script("window.scrollBy(0, 2000)")
    scroll_count+=1
    try:
        WebDriverWait(driver,1).until(EC.visibility_of_any_elements_located((By.XPATH,"//div[@class='from-now'][text()='a month ago']")))
        scroll = False
    except:
        pass
    if scroll_count > 100:
        raise Exception("Element not found in number of scrolls")
    time.sleep(3)


#scrolls back to the beggining
starting_element = driver.find_element(By.CLASS_NAME,"match-block_header")
driver.execute_script("arguments[0].scrollIntoView(true);", starting_element)




#finds all the elements that contain matches
all_ranked_matches = driver.find_elements(By.XPATH,"//div[@data-match][descendant::div[@class='queue-type'][text()='Ranked Solo']]")




#clicks on every element and so the the DOM of the elements loads and additional information can be accessed
for player in all_ranked_matches:
    bool_hodnota = True
    while bool_hodnota:
        player.click()
        try:
            WebDriverWait(driver,30).until((EC.presence_of_element_located((By.XPATH,f'//div[@class="expanded-match-card-container"][preceding-sibling::div[@data-match={str(player.get_dom_attribute("data-match"))}]]'))))
            bool_hodnota = False
        except TimeoutException:
            player.click()
            bool_hodnota = True



    
#scrolls back to the beggining again
driver.execute_script("arguments[0].scrollIntoView(true);", starting_element)
time.sleep(5)

#finds all the information needed 

from_now = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='from-now'][preceding-sibling::div[@class='queue-type'][text()='Ranked Solo']][parent::div[@class='row-one']]")))
kda_totals = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='KDA-totals'][parent::div[@class='post-stats'][preceding-sibling::div[@class='group-one'][descendant::div[@class='queue-type'][text()='Ranked Solo']]]]")))
cs_class = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='cs'][parent::div[@class='post-stats'][preceding-sibling::div[@class='group-one'][descendant::div[@class='queue-type'][text()='Ranked Solo']]]]")))
vision_score = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//span[1][parent::div[@class='vision-value'][parent::div[@class='post-stats'][preceding-sibling::div[@class='group-one'][descendant::div[@class='queue-type'][text()='Ranked Solo']]]]]"))) 
game_durations = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='game-duration'][parent::div[@class='row-three'][preceding-sibling::div[@class='row-one'][child::div[@class='queue-type'][text()='Ranked Solo']]]]")))
carry_score = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,f'//div[contains(@class,"carry-score")][preceding-sibling::div[@class="player"][child::div[@class="player-name-and-rank"][child::a[@title="{acc_name.text}"]]]]')))
damage_amount = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,f'//div[@class="damage"][preceding-sibling::div[@class="player"][child::div[@class="player-name-and-rank"][child::a[@title="{acc_name.text}"]]]][ancestor::div[@class="expanded-match-card-container"][preceding-sibling::div[@data-match][descendant::div[@class="queue-type"][text()="Ranked Solo"]]]]')))
gold_share = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,f'//div[not(@class)][preceding-sibling::div[@class="player"][child::div[@class="player-name-and-rank"][child::a[@title="{acc_name.text}"]]]][ancestor::div[@class="expanded-match-card-container"][preceding-sibling::div[@data-match][descendant::div[@class="queue-type"][text()="Ranked Solo"]]]]')))
lp_value = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,'//span[@class="lp-value"][ancestor::div[@class="match-outcome"]]')))

#makes lists for storing the info we need
kda_totals_list = []
avg_kda = []
from_now_list = []
cs_list = []
vision_score_list = []
game_duration_list = []
carry_score_list = []
damage_list = []
gold_list = []
lp_value_list = []


#adds the information into the lists as needed many different problems are fixed here thats why it looks so messy
for from_n in from_now:
    from_now_list.append(from_n.text)

for kda_total in kda_totals:
    kda_totals_list.append([i.strip() for i in kda_total.text.split("/")])
    
    if int(kda_total.text.split("/")[1]) == 0:
        avg_kda.append(round((int(kda_total.text.split("/")[0]) + int(kda_total.text.split("/")[2])),2))
    else:
        avg_kda.append(round((int(kda_total.text.split("/")[0]) + int(kda_total.text.split("/")[2])) / int(kda_total.text.split("/")[1]),2))

for cs in cs_class:
    cs_list.append([cs.text.split(" ")[0],cs.text.split(" ")[2]])

for vision in vision_score:
    vision_score_list.append(vision.text.split("\xa0")[0])

for game_duration in game_durations:
    game_duration_list.append(game_duration.text)

for carry in carry_score:
    carry_score_list.append(carry.text)
    print(carry.text)
  

for damage in damage_amount:
    damage_list.append(" ".join(damage.text.split("&nbspc;")))

for gold in gold_share:
    gold_list.append(gold.text)

for lp in lp_value:
    print(lp.find_element(By.XPATH, (8*"../")[0:-1]).get_dom_attribute("class"))
    if "match-card-container match_win" in lp.find_element(By.XPATH, (8*"../")[0:-1]).get_dom_attribute("class"): 
        lp_value_list.append(lp.get_attribute("innerText"))
    else:
        
        lp_value_list.append(f"-{lp.get_attribute("innerText")}")
    

    

#stores all the information in a dictionary format so it can make a good json format

data_dict = {"carry_score":carry_score_list[0:from_now_list.index('a month ago')],
             "cs":cs_list[0:from_now_list.index('a month ago')],
            "from_now":from_now_list[0:from_now_list.index('a month ago')],
            "kda_totals":kda_totals_list[0:from_now_list.index('a month ago')],
            "avg_kda":avg_kda[0:len(carry_score_list)],
            "vision_score":vision_score_list[0:from_now_list.index('a month ago')],
            "game_duration":game_duration_list[0:from_now_list.index('a month ago')],
            "damage":damage_list[0:len(carry_score_list)],
            "gold":gold_list[0:from_now_list.index('a month ago')],
            "lp_value":lp_value_list[0:from_now_list.index('a month ago')]
            }

#opens a json file and puts the info we need inside of it
with open("lolko_web_scraping_projekt\summoner_udaje.json","w") as summoner_udaje:
    json.dump(data_dict,summoner_udaje,indent=4)

driver.quit()

    