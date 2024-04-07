from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def search_web(search_term):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    driver.get("https://www.google.com")

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    search_query = search_term
    search_box.send_keys(search_query)

    search_box.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))

    search_results = driver.find_elements(By.XPATH, "//a[h3]")

    filtered_results = []

    for result in search_results:
        title = result.find_element(By.XPATH, ".//h3").text
        url = result.get_attribute("href")

        if title and url:
            filtered_results.append({"title": title, "url": url})

    driver.quit()
    return filtered_results


def web_pages_content(urls):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    body_texts = []

    for url in urls:
        driver.get(url)

        body_text = driver.find_element("tag name", "body").text
        body_texts.append(body_text)

    driver.quit()

    return body_texts
