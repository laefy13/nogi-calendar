from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class translate_this:

    def __init__(self, og_lang='ja',tl_lang='en', html_element='--l --r sentence_highlight',wait_time = 5):
        self.url = f'https://www.deepl.com/translator#{og_lang}/{tl_lang}'
        self.html_element = html_element
        self.wait_time = wait_time

    def get_html_content_with_selenium(self,line):
        try:
            chrome_options = Options()
            # chrome_options.add_argument('--headless')

            with webdriver.Chrome(options=chrome_options) as driver:
                driver.get(f'{self.url}/{line}')

                try:
                    wait = WebDriverWait(driver, self.wait_time)
                    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, self.html_element), ""))
                except TimeoutException:
                    # print("Timed out waiting for the element to be present or have non-empty text.")
                    pass

                html_content = driver.page_source

            return html_content

        except Exception as e:
            print(f"selenium error: {e}")
            return None

    def get_translation(self,line):
        try:
            soup = BeautifulSoup(self.get_html_content_with_selenium(line), 'html.parser')
            span_elements = soup.find_all('span', class_=self.html_element)

            if span_elements:
                return span_elements[1].text
            else:
                return 'error or something'

        except Exception as e:
            print(f"b4 error: {e}")

