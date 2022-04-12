from selenium import webdriver
import pytest
import os

root_dir = os.path.dirname(os.path.abspath(__file__))


def driver():
    return webdriver.Firefox(executable_path=os.path.join(root_dir, 'geckodriver'))


@pytest.fixture
def test_driver(driver):
    assert False
