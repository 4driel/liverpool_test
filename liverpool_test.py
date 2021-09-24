from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
import time
import unittest

class Liverpool_Test(unittest.TestCase):
    @classmethod
    def setUp(self):
        self._driver = webdriver.Chrome()
        self._driver.implicitly_wait(5)
        self._driver.get("https://www.liverpool.com.mx/tienda/home")
        self._driver.maximize_window()
        self._action = webdriver.ActionChains(self._driver)

        self.config = configparser.RawConfigParser()
        self.config.read('test.properties')
    
    def test_search(self):
        assert "Resultados" in self._search(self.config.get('Search', 'search_term'))
        time.sleep(2)
    
    def test_no_result_search(self):
        assert 'arrojó "0" resultados' in self._search(self.config.get('Search', 'dummy_term'))
        time.sleep(3)
    
    def test_advanced_search(self):
        self._search(self.config.get('Search', 'search_term'))

        brand = self.config.get('Search', 'brand')
        checkbox = self._find_element(By.XPATH, f"//label[contains(text(), '{brand}')]/preceding-sibling::div[contains(@class, 'm-checkbox')]")
        checkbox.location_once_scrolled_into_view
        time.sleep(2)
        checkbox.click()
        time.sleep(2)

        color = self.config.get('Search', 'color')
        col = self._find_element(By.CSS_SELECTOR, f"a.a-productColor__item[data-color='{color}']")
        col.location_once_scrolled_into_view
        time.sleep(2)
        col.click()
        time.sleep(2)

        model = self.config.get('Search', 'model')
        mod = self._find_element(By.XPATH, f"//h5[contains(text(), '{model}')]")
        mod.location_once_scrolled_into_view
        time.sleep(2)
        mod.click()
        time.sleep(2)

        assert self._find_element(By.CSS_SELECTOR, f"button.a-btn[id='opc_pdp_buyNowButton']")
        time.sleep(3)

    def test_buy_tv(self):
        self._search('tv')

        brand = self.config.get('TV', 'brand')
        checkbox = self._find_element(By.XPATH, f"//label[contains(text(), '{brand}')]/preceding-sibling::div[contains(@class, 'm-checkbox')]")
        checkbox.location_once_scrolled_into_view
        time.sleep(2)
        checkbox.click()
        time.sleep(2)

        size = self.config.get('TV', 'size')
        size_cb = self._find_element(By.XPATH, f"//label[contains(text(), '{size}')]/preceding-sibling::div[contains(@class, 'm-checkbox')]")
        time.sleep(2)
        size_cb.click()
        time.sleep(2)

        price_range = self.config.get('TV', 'price_range')
        price = self._find_element(By.XPATH, f"//label[contains(text(), '{price_range}')]/preceding-sibling::div[contains(@class, 'm-checkbox')]")
        price.location_once_scrolled_into_view
        time.sleep(2)
        price.click()
        time.sleep(2)

        model = self.config.get('TV', 'model')
        mod = self._find_element(By.XPATH, f"//h5[contains(text(), '{model}')]")
        time.sleep(2)
        mod.click()
        time.sleep(2)

        assert self._find_element(By.CSS_SELECTOR, f"button.a-btn[id='opc_pdp_buyNowButton']")
        time.sleep(3)

    def test_create_cust_account(self):
        login = self._find_element(By.CSS_SELECTOR, f"span.a-header__topLink")
        login.click()

        create_acc = self._find_element(By.XPATH, f"//a[contains(text(), 'Crear cuenta')]")
        create_acc.click()

        email_f = self._find_element(By.CSS_SELECTOR, f"input#email")
        email_f.send_keys(self.config.get('Customer Account', 'email'))

        pwd = self._find_element(By.CSS_SELECTOR, f"input#password")
        pwd.send_keys(self.config.get('Customer Account', 'password'))

        button = self._find_element(By.CSS_SELECTOR, f"button[name='action']")
        button.click()
        time.sleep(3)

        name_el = self._find_element(By.CSS_SELECTOR, f"input[name='user_firstName']")
        name_el.send_keys(self.config.get('Customer Account', 'names'))

        last_name_f = self._find_element(By.CSS_SELECTOR, f"input[name='user_lastName']")
        last_name_f.send_keys(self.config.get('Customer Account', 'last_name_father'))

        last_name_m = self._find_element(By.CSS_SELECTOR, f"input[name='user_MotherName']")
        last_name_m.send_keys(self.config.get('Customer Account', 'last_name_mother'))

        bday = self._find_element(By.CSS_SELECTOR, f"select#daySelectorLabel")
        bday.send_keys(self.config.get('Customer Account', 'birth_day'))

        b_month = self._find_element(By.CSS_SELECTOR, f"select#monthSelectorLabel")
        b_month.send_keys(self.config.get('Customer Account', 'birth_month'))

        b_year = self._find_element(By.CSS_SELECTOR, f"select#yearSelectorLabel")
        b_year.send_keys(self.config.get('Customer Account', 'birth_year'))

        gender = self._find_element(By.CSS_SELECTOR, f"input#{self.config.get('Customer Account', 'gender')}")
        gender.click()

        create_btn = self._find_element(By.CSS_SELECTOR, f"button.a-btn")
        create_btn.location_once_scrolled_into_view
        time.sleep(2)
        create_btn.click()

        cell = self._find_element(By.CSS_SELECTOR, f"input#phone")
        cell.send_keys(self.config.get('Customer Account', 'cellphone'))

        cell_btn = self._find_element(By.XPATH, f"//button[contains(text(), 'Continuar')]")
        cell_btn.click()

        time.sleep(5)
        assert True

    def _search(self, keyword):
        input = self._find_element(By.CSS_SELECTOR, "input.search-bar")
        input.clear()
        input.send_keys(keyword)
        input.send_keys(Keys.ENTER)

        time.sleep(1)

        if self._driver.find_elements_by_css_selector("span.searchNum-result"):
            res = self._find_element(By.CSS_SELECTOR, "span.searchNum-result").text
            print(f'res: {res}')
        else:
            res = self._find_element(By.CSS_SELECTOR, "h1.a-headline__results").text
            print(f'res: {res}')
        return res

    def _find_element(self, selector_type, selector):
        element = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((selector_type, selector)))
        return element
    
    @classmethod
    def tearDown(self):
        pass
        self._driver.quit()
        

if __name__ == "__main__":
    unittest.main()