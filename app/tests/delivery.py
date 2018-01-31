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
        for x in xrange(0, 100):
            driver = self.driver
            email_part = "caio" + str(uuid.uuid4())
            email = email_part[:8] + "@gmail.com"
            driver.get(self.base_url + "/login/cadastro")
            driver.find_element_by_id("first_name").clear()
            driver.find_element_by_id("first_name").send_keys("Felipe" + str(uuid.uuid4())[:4])
            driver.find_element_by_id("last_name").clear()
            driver.find_element_by_id("last_name").send_keys("Barboza" + str(uuid.uuid4())[:4])
            driver.find_element_by_id("cpf").clear()
            cpf = generate_cpf()
            driver.find_element_by_id("cpf").send_keys(cpf)
            driver.find_element_by_id("birthday").clear()
            driver.find_element_by_id("birthday").send_keys('19/01/1995')
            driver.find_element_by_id("phone").clear()
            driver.find_element_by_id("phone").send_keys('83988776655')
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

            driver.get(self.base_url + "/dcher")

            driver.find_element_by_xpath(
                "//img[contains(@src,'https://deliverymuch.com.br/media/59fa190a58c3f.png')]").click()
            driver.find_element_by_name("dm-product-add-287199").click()
            driver.find_element_by_css_selector("label").click()
            driver.find_element_by_name("dm-product-add-287201").click()
            driver.find_element_by_xpath("//div[@id='dm-pm-groups']/div[3]/label").click()
            driver.find_element_by_id("dm-pm-add-to-cart").click()
            driver.find_element_by_id("dm-cm").click()
            time.sleep(1)
            driver.find_element_by_link_text("Finalizar Compra").click()
            time.sleep(1)
            driver.find_element_by_name("delivery-method").click()
            driver.find_element_by_css_selector("label.dm-ck-radio").click()
            driver.find_element_by_id("pay-money").click()
            time.sleep(1)
            driver.find_element_by_css_selector("div.dm-ck-payment-types > label.dm-ck-radio").click()
            driver.find_element_by_id("discount-code").clear()
            driver.find_element_by_id("discount-code").send_keys("primeira")
            driver.find_element_by_css_selector("span.ladda-label").click()
            time.sleep(3)
            driver.find_element_by_css_selector("#dm-ck-form-submit > span.ladda-label").click()
            # driver.find_element_by_link_text("Kit Com 10 Dindins").click()
            # driver.find_element_by_css_selector("div.dm-product > img.img-responsive").click()
            # driver.find_element_by_xpath("(//input[@name='dm-product-add-86652'])[2]").click()
            # driver.find_element_by_xpath("//div[@id='dm-pm-groups']/div[2]/label[2]").click()
            # driver.find_element_by_xpath("(//input[@name='dm-product-add-86653'])[3]").click()
            # driver.find_element_by_xpath("//div[@id='dm-pm-groups']/div[3]/label[3]").click()
            # driver.find_element_by_xpath("(//input[@name='dm-product-add-86654'])[4]").click()
            # driver.find_element_by_xpath("//div[@id='dm-pm-groups']/div[4]/label[4]").click()
            # driver.find_element_by_xpath("(//input[@name='dm-product-add-86655'])[6]").click()
            # driver.find_element_by_xpath("//div[@id='dm-pm-groups']/div[5]/label[6]").click()
            # driver.find_element_by_xpath("(//input[@name='dm-product-add-86656'])[7]").click()
            # driver.find_element_by_xpath("//div[@id='dm-pm-groups']/div[6]/label[7]").click()
            # driver.find_element_by_xpath("(//input[@name='dm-product-add-86657'])[10]").click()
            # driver.find_element_by_xpath("//div[@id='dm-pm-groups']/div[7]/label[10]").click()
            # driver.find_element_by_xpath("(//input[@name='dm-product-add-86658'])[14]").click()
            # driver.find_element_by_xpath("//div[@id='dm-pm-groups']/div[8]/label[14]").click()
            # driver.find_element_by_xpath("(//input[@name='dm-product-add-86660'])[14]").click()
            # driver.find_element_by_xpath("//div[@id='dm-pm-groups']/div[10]/label[14]").click()
            # driver.find_element_by_id("dm-pm-add-to-cart").click()
            # driver.find_element_by_id("dm-cm").click()
            # time.sleep(1)
            # driver.find_element_by_link_text("Finalizar Compra").click()
            # time.sleep(1)
            # driver.find_element_by_name("delivery-method").click()
            # driver.find_element_by_css_selector("label.dm-ck-radio").click()
            # driver.find_element_by_id("pay-money").click()
            # time.sleep(1)
            # driver.find_element_by_css_selector("div.dm-ck-payment-types > label.dm-ck-radio").click()
            # driver.find_element_by_id("discount-code").clear()
            # driver.find_element_by_id("discount-code").send_keys("primeira")
            # driver.find_element_by_css_selector("span.ladda-label").click()
            # time.sleep(3)
            # driver.find_element_by_css_selector("#dm-ck-form-submit > span.ladda-label").click()
            try:
                self.assertEqual("Aguardando", driver.find_element_by_id("dm-tk-status-text").text)
            except AssertionError as e:
                self.verificationErrors.append(str(e))
            time.sleep(30)
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
