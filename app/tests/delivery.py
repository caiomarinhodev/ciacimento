# -*- coding: utf-8 -*-
import uuid

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from pycpfcnpj import gen


def generate_cpf():
    return '%s' % gen.cpf_with_punctuation()


class Delivery(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://deliverymuch.com.br"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_delivery(self):
        driver = self.driver
        email_part = "caio" + str(uuid.uuid4())
        email = email_part[:8] + "@gmail.com"
        driver.get(self.base_url + "/login/cadastro")
        driver.find_element_by_id("first_name").clear()
        driver.find_element_by_id("first_name").send_keys("Caio")
        driver.find_element_by_id("last_name").clear()
        driver.find_element_by_id("last_name").send_keys("Marinho")
        driver.find_element_by_id("cpf").clear()
        cpf = generate_cpf()
        driver.find_element_by_id("cpf").send_keys(cpf)
        driver.find_element_by_id("birthday").clear()
        driver.find_element_by_id("birthday").send_keys('19/01/1995')
        driver.find_element_by_id("phone").clear()
        driver.find_element_by_id("phone").send_keys('83988731795')
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(email)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("oficinag3")
        driver.find_element_by_id("password_confirmation").clear()
        driver.find_element_by_id("password_confirmation").send_keys("oficinag3")
        time.sleep(2)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_xpath("//div[4]/div").click()
        try:
            self.assertEqual("Tudo certo!", driver.find_element_by_css_selector("strong").text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
            print('Erro, nao foi possivel criar o email')

        print('email: ', email)
        print('senha: ', 'oficinag3')
        print('codigo: ', 'primeira')

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
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
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
