from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class Scrape_this:

    def __init__(self, headless,html_element='m--scone__ttl',wait_time = 5,url='https://www.nogizaka46.com/s/n46/media/list?ima=4039&dy=202402'):
        self.url = url
        self.html_element = html_element
        self.wait_time = wait_time
        self.headless = headless



    def get_html_content_with_selenium(self):
        try:
            fox_options = Options()
            if self.headless:
                fox_options.add_argument('--headless')

            with webdriver.Firefox(options=fox_options) as driver:
                driver.get(f'{self.url}')

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

    def get_sched(self):
        
        # for date get all <div class="m--scone js-pos a--tx is-v">
        # then loop though all the scone shit then fucking get all p within that shit then dict within dict
        try:
            soup = BeautifulSoup(self.get_html_content_with_selenium(), 'html.parser')
            
            sc_day_hd_elements = soup.find_all('div', class_='sc--day')
            sched = {}

            for element in sc_day_hd_elements:
                div_id = element.find('p', class_='sc--day__d').get_text(strip=True)

                day_elements = []
                
                scone_elements = element.find_all('div', class_='m--scone')
                for count,scone in enumerate(scone_elements):
                    try:
                        time = scone.find('p', class_='m--scone__st').get_text(strip=True)
                    except:
                        time = scone.find('p', class_='m--scone__cat__name').get_text(strip=True)
                    p = scone.find('p', class_=self.html_element).get_text(strip=True)
                    day_elements.append({time:p})
                sched[div_id] = day_elements
            return sched
        except Exception as e:
            print(f"b4 error: {e}")
    