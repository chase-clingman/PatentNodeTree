from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException

import time

def visit_links(url, depth=0, max_depth=3):
    if depth >= max_depth:
        print(f'Max depth of {max_depth} reached.')
        return

    driver = webdriver.Chrome(executable_path=r'/path/to/chromedriver') 
    driver.maximize_window()
    driver.get(url)
    for attempt in range(5):
        try:
            time.sleep(2)
            continuity_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'link_app-data-continuity')))
            continuity_button.click()
            time.sleep(2)
            break  # If the button was clicked successfully, break the loop
        except TimeoutException:
            if attempt < 4:  # If this wasn't the last attempt, refresh the page and try again
                driver.refresh()
            else:  # If this was the last attempt, re-raise the exception
                raise

    print('Depth:', depth)
    # Select only the links that come after the "Child data" header
    links = driver.find_elements(By.XPATH, "//h4[text()='Child data']/following::a[@id='link_continuity-child-childAppTxt']")

    for i in range(len(links)):
        links = driver.find_elements(By.XPATH, "//h4[text()='Child data']/following::a[@id='link_continuity-child-childAppTxt']")
        link = links[i]
        parent = link.find_element(By.XPATH, '..') 
        try:
            next_6_td_elements = parent.find_elements(By.XPATH, './following-sibling::td')
            print('  ' * depth + 'Continuity: ' + link.text + ' - ' + ' | '.join(td.text for td in next_6_td_elements))
        except Exception as e:
            print(f"No next 'td' siblings found for {link.text}. Error: {str(e)}")

        try:
            child_application_number = link.text
            child_application_number = ''.join(filter(str.isdigit, child_application_number))  # Retain only digits
            child_url = 'https://patentcenter.uspto.gov/applications/' + child_application_number
            
            visit_links(child_url, depth=depth + 1, max_depth=max_depth)
        except Exception as e:
            print(f"Unable to visit child page for {link.text}. Error: {str(e)}")

    driver.quit()

visit_links('https://patentcenter.uspto.gov/applications/15442229')
