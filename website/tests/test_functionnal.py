from selenium import webdriver
from website import app
import os
from flask_testing import LiveServerTestCase
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import time

root_dir = os.path.dirname(os.path.abspath(__file__))


class Test_truc(LiveServerTestCase):
    def create_app(self):
        app.testing = True
        app.config['DEBUG'] = True
        app.config['LIVESERVER_PORT'] = 8943
        return app

    def setUp(self):
        self.driver = webdriver.Firefox(service=Service(os.path.join(root_dir, 'geckodriver')))
        self.action = ActionChains(self.driver)

    def tearDown(self) -> None:
        self.driver.quit()

    def get_elt(self, selector):
        return self.driver.find_element(by=By.CSS_SELECTOR, value=selector)

    def test_init(self):
        self.driver.get(self.get_server_url())
        assert self.driver.current_url == 'http://localhost:8943/'

    def test_main_button(self):
        self.driver.get(self.get_server_url())
        self.driver.implicitly_wait(3)
        map_button = self.get_elt('.main_button')
        self.action.move_to_element(map_button)
        map_button.click()
        time.sleep(2)
        assert self.driver.current_url == 'http://localhost:8943/map_desc/1'
        self.driver.implicitly_wait(10)
