from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time

# Install ChromeDriver
chromedriver_autoinstaller.install()

# Create a new instance of the Chrome driver
opt = webdriver.ChromeOptions()
opt.add_argument("--start-maximized")
driver = webdriver.Chrome(options=opt)
driver.implicitly_wait(10)
act = ActionChains(driver)

# Navigate to the given URL
driver.get('https://www.imdb.com/search/name/')

def scroll_to_element_and_click(driver, by, value):
    try:
        element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((by, value))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        WebDriverWait(driver, 5).until(
            EC.visibility_of(element)
        )
        try:
            element.click()
        except Exception:
            driver.execute_script("arguments[0].click();", element)
    except Exception as e:
        print(f"Error: {e}")
        # Save the current page source and screenshot for debugging
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot("screenshot.png")
        raise e

def wait_for_element_and_send_keys(driver, by, value, keys):
    element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((by, value))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    WebDriverWait(driver, 5).until(
        EC.visibility_of(element)
    )
    element.send_keys(keys)

# NAME
scroll_to_element_and_click(driver, By.XPATH, '//*[@id="nameTextAccordion"]/div[1]/label/span[1]/div')
wait_for_element_and_send_keys(driver, By.NAME, 'name-text-input', 'Paul Walker')
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

# BIRTHDATE
scroll_to_element_and_click(driver, By.XPATH, '//*[@id="birthDateAccordion"]/div[1]/label')
wait_for_element_and_send_keys(driver, By.NAME, 'birth-date-start-input', '09/12/1973')
wait_for_element_and_send_keys(driver, By.NAME, 'birth-date-end-input', '09/12/1973')
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

# BIRTHDAY
scroll_to_element_and_click(driver, By.XPATH, '//*[@id="birthdayAccordion"]/div[1]/label')
wait_for_element_and_send_keys(driver, By.NAME, 'birthday-input', '04-04')
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

# AWARDS & RECOGNITION
scroll_to_element_and_click(driver, By.XPATH, '//*[@id="awardsAccordion"]/div[1]/label')
scroll_to_element_and_click(driver, By.XPATH, '//*[@id="accordion-item-awardsAccordion"]/div/section/button[2]')  # Best Actor-Nominated
scroll_to_element_and_click(driver, By.XPATH, '//*[@id="accordion-item-awardsAccordion"]/div/section/button[14]')  # Oscar-Winning
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

# PAGE TOPIC
scroll_to_element_and_click(driver, By.XPATH, '//*[@id="pageTopicsAccordion"]/div[1]/label')
scroll_to_element_and_click(driver, By.XPATH, '//*[@id="accordion-item-pageTopicsAccordion"]/div/div/section/button[1]')  # Award Nominations
scroll_to_element_and_click(driver, By.XPATH, '//*[@id="accordion-item-pageTopicsAccordion"]/div/div/section/button[2]')  # Biography
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

# DROP DOWN
try:
    dropdown = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="within-topic-dropdown-id"]'))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
    dropdown.click()
    options = dropdown.find_elements(By.TAG_NAME, 'option')
    for option in options:
        if option.text == "Biography":
            option.click()
            break
except Exception as e:
    print("Biography not selected", e)

wait_for_element_and_send_keys(driver, By.NAME, 'within-topic-input', "Movies")
act.send_keys(Keys.TAB).perform()
act.send_keys(Keys.ENTER).perform()

# DEATH DATE
act.send_keys(Keys.TAB).perform()
act.send_keys('30/11/2013').perform()  # Corrected the death date format and value
act.send_keys(Keys.TAB).send_keys('30/11/2013').perform()
act.send_keys(Keys.ENTER).perform()

# GENDER IDENTITY
scroll_to_element_and_click(driver, By.XPATH, '//*[@id="genderIdentityAccordion"]/div[1]/label')
scroll_to_element_and_click(driver, By.XPATH, '//*[@id="accordion-item-genderIdentityAccordion"]/div/section/button[1]')
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

# CREDITS
scroll_to_element_and_click(driver, By.XPATH, '//*[@id="filmographyAccordion"]/div[1]/label')
wait_for_element_and_send_keys(driver, By.XPATH, '//*[@id="accordion-item-filmographyAccordion"]/div/div/div/div[1]/input', 'I Am Heath Ledger')
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
act.send_keys(Keys.DOWN).perform()
act.send_keys(Keys.ENTER).perform()

# ADULT NAME
scroll_to_element_and_click(driver, By.XPATH, '//*[@id="adultNamesAccordion"]/div[1]/label')
scroll_to_element_and_click(driver, By.ID, 'include-adult-names')
act.send_keys(Keys.ENTER).perform()

# 2 times PAGE_UP for SEARCH.
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP, Keys.PAGE_UP)

# SEARCH BUTTON
try:
    scroll_to_element_and_click(driver, By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[1]/button[2]')
except Exception as e:
    print(f"Error clicking search button: {e}")
    # Save the current page source and screenshot for debugging
    with open("page_source_after_error.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    driver.save_screenshot("screenshot_after_error.png")

# Collapse all
try:
    close = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[1]/div/button'))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", close)
    act.double_click(close).perform()
except Exception as e:
    print(f"Error collapsing sections: {e}")

# Paul Walker
try:
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.LINK_TEXT, '1. Paul Walker'))
    ).click()
except Exception as e:
    print(f"Error clicking on Paul Walker link: {e}")

# Close the browser
driver.quit()
