from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
import re
import json
import random
import pandas as pd


class Crawler:
    def __init__(self, userid_min, userid_max, no_users, executable_path=None, data_path='../data'):
        # Use both api and html parser method to crawl data

        # Init variables
        self._userid_max = userid_max
        self._userid_min = userid_min
        self._no_users = no_users
        self._data_path = data_path
        self._user_ids = random.sample(
            range(self._userid_min, self._userid_max + 1), self._no_users)

        # Create driver
        option = Options()
        option.add_argument('headless')
        option.add_argument('disable-gpu')
        self._driver = None
        if executable_path:
            self._driver = Chrome(service=Service(
                executable_path), options=option)
        else:
            self._driver = Chrome(options=option)

        # Get client id
        self._client_id = self._get_client_id()

    def _get_client_id(self):
        # Use selenium to get client id
        # Get client id of the logged-in user in the browser
        self._driver.get('https://soundcloud.com')
        log = self._driver.get_log('browser')
        client_id = re.search(r"client_id=(.*?)\&", log[0]['message']).group(1)
        return client_id

    def _get_user_info(self, path):
        # Get user data and store in user.csv
        jsondata = []
        for user_id in self._user_ids:
            response = None
            response = requests.get(
                f'https://api-v2.soundcloud.com/users/{user_id}?client_id={self._client_id}')
            if response.ok:
                jsondata.append(response.json())
        data = pd.DataFrame(jsondata)
        data.to_csv(path + '/user.csv',index=False)

    def _get_track_data(self, path):
        data = pd.DataFrame('')
        for user_id in self._user_ids:
            response = requests.get(
                f"https://api-v2.soundcloud.com/users/{user_id}/tracks?client_id={self._client_id}")
            if response.ok:
                response.json()['collection']

    def get_data(self,  path='./data'):
        self._get_user_info(path)
        self._terminate()

    def _terminate(self):
        self._driver.close()
