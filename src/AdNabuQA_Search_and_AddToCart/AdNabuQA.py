'''
Created on 05-Apr-2026

@author: aithe
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
from HtmlTestRunner import HTMLTestRunner


class AdNabuQA(unittest.TestCase):
    URL = "https://adnabu-store-assignment1.myshopify.com/"
    PASSWORD_URL = "https://adnabu-store-assignment1.myshopify.com/password"
    STORE_PASSWORD = "AdNabuQA"
    SEARCH_ITEM = "Snowboard"

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def open_site(self):
        self.driver.get(self.URL)
        self.enter_password_if_needed()

    def enter_password_if_needed(self):
        if "/password" in self.driver.current_url:
            password_box = self.wait.until(
                EC.visibility_of_element_located((By.ID, "password"))
            )
            password_box.clear()
            password_box.send_keys(self.STORE_PASSWORD)

            enter_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            enter_button.click()

    def search_for_product(self, search_item):
        search_icon = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//summary[contains(@class,'header__icon--search')]")
            )
        )
        search_icon.click()

        search_box = self.wait.until(
            EC.visibility_of_element_located((By.ID, "Search-In-Modal"))
        )
        search_box.clear()
        search_box.send_keys(search_item + Keys.ENTER)

    def add_to_cart(self):
        product = self.wait.until(
            EC.element_to_be_clickable((By.ID, "CardLink--7801364480090"))
        )
        product.click()

        add_to_cart_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "ProductSubmitButton-template--19850788667482__main")
            )
        )
        add_to_cart_button.click()

    def verify_cart_opened(self):
        cart_heading = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="CartDrawer"]/div[2]/div[1]/h2')
            )
        )
        self.assertEqual(cart_heading.text.strip(), "Your cart")

    def test_search_and_add_to_cart(self):
        self.open_site()
        self.search_for_product(self.SEARCH_ITEM)
        self.add_to_cart()
        self.verify_cart_opened()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(
        testRunner=HTMLTestRunner(
            output="reports",
            report_name="AdNabu_Test_Report",
            combine_reports=True
        ),
        verbosity=2
    )