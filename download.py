from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time


class Download:
    def __init__(self, directory):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome('chromedriver.exe', chrome_options=self.options)

        self.driver.command_executor._commands["send_command"] = (
            "POST",
            '/session/$sessionId/chromium/send_command'
        )
        self.params = {
            'cmd': 'Page.setDownloadBehavior',
            'params': {
                'behavior': 'allow',
                'downloadPath': directory
            }
        }
        self.driver.execute("send_command", self.params)

    def download_url(self, url):
        self.driver.get(url)
        self.driver.find_element_by_xpath('//*[@id="uc-download-link"]').click()

    def close_dirver(self):
        self.driver.close()
        self.driver.quit
        print('chrome driver closed')
