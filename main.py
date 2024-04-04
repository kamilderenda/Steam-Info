from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

PATH='https://steamdb.info'

if __name__ == '__main__':
    nc = webdriver.ChromeOptions()
    nc.add_experimental_option('detach', True)

    driver = webdriver.Chrome(options=nc)
    driver.get(PATH)
    most_played_games = driver.find_element(By.XPATH,'//a[contains(@href, "/charts/")]')
    most_played_games.click()
    table=driver.find_element(By.ID,'table-apps')
    tbody=table.find_element(By.TAG_NAME,'tbody')
    rows = tbody.find_elements(By.TAG_NAME,'tr')
    steam_info_list = []

    for i, row in enumerate(rows):
        game_name_element = row.find_elements(By.TAG_NAME, 'td')[2]
        game_name = game_name_element.text

        current = row.find_elements(By.TAG_NAME, 'td')[3]
        current = current.text

        peak24h = row.find_elements(By.TAG_NAME, 'td')[4]
        peak24h = peak24h.text

        alltime_peak = row.find_elements(By.TAG_NAME, 'td')[5]
        alltime_peak = alltime_peak.text

        data_dict = {'name': game_name,
                     'Current Players': current,
                     '24h Peak': peak24h,
                     'All-Time Peak': alltime_peak}

        steam_info_list.append(pd.DataFrame(data_dict, index=[i]))

    steam_info = pd.concat(steam_info_list, ignore_index=True)


    steam_info.to_csv('Steam_Info.csv', sep=';', index=False, encoding='utf-8')

    print(steam_info)

    driver.quit()
