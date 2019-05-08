from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.


class loginTests(LiveServerTestCase):
        selenium = self.selenium
        #get the login page
        selenium.get('http://127.0.0.1:8000/')
        #the login form html elements are defined below
        userName = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        logIn = selenium.find_element_by_id('login')

        def blank(self):
            #data to test the login form with
            #test for empty data
            userName.send_keys('')
            password.send_keys('')
            login.send_keys(Keys.RETURN)
            assert 'Check your email' in selenium.page_source


        def capitalise(self):
            #test for case sensitivity on correct details
            userName.send_keys('EDUCATION')
            password.send_keys('EDUCATION')
            login.send_keys(keys.RETURN)
            assert 'Check your email' in selenium.page_source

        def badDetails(self):
            #test for wrong passwords
            userName.send_keys('thisisfake')
            password.send_keys('notrealpassword')

            login.send_keys(keys.RETURN)
            assert 'Check your email' in selenium.page_source


        
