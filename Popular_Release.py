from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

PATH='https://steamdb.info/upcoming/?lastweek&sort=peak_desc'

if __name__ == '__main__':
    nc = webdriver.ChromeOptions()
    nc.add_experimental_option('detach', True)

    driver = webdriver.Chrome(options=nc)
    driver.get(PATH)

    table=driver.find_element(By.ID,'DataTables_Table_0_wrapper')
    tbody=table.find_element(By.TAG_NAME,'tbody')
    rows = tbody.find_elements(By.TAG_NAME,'tr')
    steam_info_list = []

    for i, row in enumerate(rows):
        game_name_element = row.find_elements(By.TAG_NAME, 'td')[2]
        game_name = game_name_element.text.split('\n')[0]

        dis_ris = row.find_elements(By.TAG_NAME, 'td')[3]
        dis_ris = dis_ris.text

        price= row.find_elements(By.TAG_NAME, 'td')[4]
        price = price.text

        Rating= row.find_elements(By.TAG_NAME, 'td')[5]
        Rating = Rating.text

        release=row.find_elements(By.TAG_NAME, 'td')[6]
        release=release.text

        follows= row.find_elements(By.TAG_NAME, 'td')[7]
        follows= follows.text

        online= row.find_elements(By.TAG_NAME, 'td')[8]
        online = online.text

        peak= row.find_elements(By.TAG_NAME, 'td')[6]
        peak= peak.text

        data_dict = {'name': game_name,
                     'discount/raise': dis_ris,
                     'Price': price,
                     'Rating': Rating,
                     'Release': release,
                     'Follows': follows,
                     'Online': online,
                     'Peak': peak
                     }

        steam_info_list.append(pd.DataFrame(data_dict, index=[i]))

    steam_info = pd.concat(steam_info_list, ignore_index=True)


    steam_info.to_csv('Popular_Releases.csv', sep=';', index=False, encoding='utf-8')

    print(steam_info)

    driver.quit()
