### FYI - unless you know what you're doing with Python, 
# this script will not run and will be timed out by Twitch Tracker. 
# You can add time.sleep(10) to pause 10 seconds... but that doens't always
# solve the problem :(
# Also, I use Jupyter Notebooks for my Python needs, so this may work a biot differently


# import all libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
     

# couldn't find the ChromeDriver on my machine...
#driver = webdriver.Chrome('chromedriver.exe')

# so I installed it everytime I run the script (need to change this)
driver = webdriver.Chrome(ChromeDriverManager().install())


# this will open a new tab and target the website
# pause for 10 seconds to stop "bot activity" feelings
# time.sleep(10)
driver.get('https://twitchtracker.com/learnwithleon/streams')


# pause for 10 seconds to stop "bot activity" feelings
# time.sleep(10)




# this is where all of the data will be located orgininally
date_list = []
avg_duration_list = []
avg_ccv_list = []
max_ccv_list = []
followers_list = []
title_list = []

# range must be modified for increasing number of pages in pagination... currently 8
for pages in range(1, 8): 
    
    # select the page number in the pagination that you want to collect data from
    next_page = driver.find_element_by_xpath(f"//div[@id='streams_wrapper']/div/ul/li[{pages}]/a")
    
    # if targeted corretly, click the pagination number
    next_page.click()
    
    
    # this is targeting the specific td on the page for the data
    date = driver.find_elements_by_xpath('//tbody/tr/td[1]')
    avg_duration = driver.find_elements_by_xpath('//tbody/tr/td[2]')
    avg_ccv = driver.find_elements_by_xpath('//tbody/tr/td[3]')
    max_ccv = driver.find_elements_by_xpath('//tbody/tr/td[4]')
    followers = driver.find_elements_by_xpath('//tbody/tr/td[5]')
    title = driver.find_elements_by_xpath('//tbody/tr/td[7]')
    
    
    for num in range(len(date)):
        date_list.append(date[num].text)
    
    for num in range(len(avg_duration)):
        avg_duration_list.append(avg_duration[num].text)

    for num in range(len(avg_ccv)):
        avg_ccv_list.append(avg_ccv[num].text)

    for num in range(len(max_ccv)):
        max_ccv_list.append(max_ccv[num].text)

    for num in range(len(followers)):
        followers_list.append(followers[num].text)

    for num in range(len(title)):
        title_list.append(title[num].text)  
        



# pop all the information into a dataframe
ALL_PAGES = pd.DataFrame({"date": date_list, 
                       "duration_hrs": avg_duration_list,
                       "avg_ccv": avg_ccv_list, 
                       "max_ccv": max_ccv_list,
                       "followers": followers_list,
                       "title": title_list})

# Check it out. Does it look right? 
ALL_PAGES.head()



# clean up the information  abity
# strip the hrs and commas
for view in range(len(ALL_PAGES)):
    ALL_PAGES['duration_hrs'][view] = float(ALL_PAGES['duration_hrs'][view].replace(" hrs",""))
    ALL_PAGES['avg_ccv'][view] = int(ALL_PAGES['avg_ccv'][view].replace(",",""))
    ALL_PAGES['max_ccv'][view] = int(ALL_PAGES['max_ccv'][view].replace(",",""))
    ALL_PAGES['followers'][view] = int(ALL_PAGES['followers'][view].replace(",",""))

# look any better?    
ALL_PAGES  


# import json library and export the data to a json file

import json
ALL_PAGES_json = ALL_PAGES.to_json(r'/Users/jacobgood/Desktop/100Devs-Stuff/webScraping/exported_data.json', orient="records")
