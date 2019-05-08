from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.


class loginTests(LiveServerTestCase):
        def setUp(self):
            self.selenium = webdriver.Chrome('C:/Users/Billy/Documents/GitHub/chromedriver.exe')
            super(loginTests, self).setUp()
            #the login form html elements are defined below
            

        def tearDown(self):
            self.selenium.quit()
            super(loginTests, self).tearDown()


        #test for empty data
        def test_blankCheck(self):
            selenium = self.selenium
            selenium.get('http://127.0.0.1:8000/')
            userName = selenium.find_element_by_id('id_username')
            password = selenium.find_element_by_id('id_password')
            logIn = selenium.find_element_by_id('login')
            #data to test the login form with
            userName.send_keys('')
            password.send_keys('')
            logIn.send_keys(Keys.RETURN)
            #if element is still there login didnt work
            assert selenium.find_element_by_id('id_username').is_displayed() is True
        #test for case sensitivity on correct details
        def test_capitalise(self):
            selenium = self.selenium
            selenium.get('http://127.0.0.1:8000/')
            userName = selenium.find_element_by_id('id_username')
            password = selenium.find_element_by_id('id_password')
            logIn = selenium.find_element_by_id('login')
            #data to test the login form with
            userName.send_keys('EDUCATION')
            password.send_keys('EDUCATION')
            logIn.send_keys(Keys.RETURN)
            #if element is still there login didnt work
            assert selenium.find_element_by_id('id_username').is_displayed() is True
        #test for wrong passwords
        def test_badDetails(self):
            selenium = self.selenium
            selenium.get('http://127.0.0.1:8000/')
            userName = selenium.find_element_by_id('id_username')
            password = selenium.find_element_by_id('id_password')
            logIn = selenium.find_element_by_id('login')
            #data to test the login form with
            userName.send_keys('thisisfake')
            password.send_keys('notrealpassword')
            logIn.send_keys(Keys.RETURN)
            #if element is still there login didnt work
            assert selenium.find_element_by_id('id_username').is_displayed() is True

        
