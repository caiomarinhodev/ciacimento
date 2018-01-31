# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Ap(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://deliverymuch.com.br/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_ap(self):
        driver = self.driver
        driver.get(self.base_url + "/dcher")
        driver.find_element_by_xpath("//img[contains(@src,'https://deliverymuch.com.br/media/59fa190a58c3f.png')]").click()
        driver.find_element_by_name("dm-product-add-287199").click()
        driver.find_element_by_css_selector("label").click()
        driver.find_element_by_name("dm-product-add-287201").click()
        driver.find_element_by_xpath("//div[@id='dm-pm-groups']/div[3]/label").click()
        driver.find_element_by_id("dm-pm-add-to-cart").click()
        driver.find_element_by_id("dm-cm").click()
        driver.find_element_by_link_text("Finalizar Compra").click()
        driver.find_element_by_name("delivery-method").click()
        driver.find_element_by_css_selector("label.dm-ck-radio").click()
        driver.find_element_by_id("pay-money").click()
        driver.find_element_by_css_selector("div.dm-ck-payment-types > label.dm-ck-radio").click()
        driver.find_element_by_id("discount-code").clear()
        driver.find_element_by_id("discount-code").send_keys("primeira")
        driver.find_element_by_css_selector("span.ladda-label").click()
        driver.find_element_by_css_selector("#dm-ck-form-submit > span.ladda-label").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
