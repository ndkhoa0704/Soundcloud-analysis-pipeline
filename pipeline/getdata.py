from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
import requests
import re
import json
import random
import pandas as pd


class Crawler:

    def __init__(
        self,
        userid_min: int,
        userid_max: int,
        no_users: int,
        no_tracks_liked: int,
        no_tracks_created: int,
        executable_path: str = None,
        data_path: str = '../data'
    ):
        '''
        Use both api and html parser method to crawl data
        Args:
        userid_min: lower-bound of user id number
        userid_max: upper-bound of user id number
        no_users: number of users to be crawled
        no_tracks_liked: number of liked tracks to be crawled for each user
        no_tracks_created: number of created tracks to be crawled for each user
        executable_path: path to webdriver
        data_path: path to folder to save data
        '''

        # Init variables
        self._userid_max = userid_max
        self._userid_min = userid_min
        self._no_users = no_users
        self._data_path = data_path
        self._no_tracks_liked = no_tracks_liked
        self._no_tracks_created = no_tracks_created

        self._user_ids = random.sample(
            range(self._userid_min, self._userid_max + 1), self._no_users)

        # Create driver
        option = Options()
        option.add_argument('headless')
        option.add_argument('disable-gpu')
        self._driver = None
        while True:
            try:
                if executable_path:
                    self._driver = Chrome(service=Service(
                        executable_path), options=option)
                else:
                    self._driver = Chrome(options=option)
            except WebDriverException:
                pass
            else:
                break

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
        data.to_csv(path + '/user.csv', index=False)

    def _get_track_data(self, path):
        jsondata = []
        for user_id in self._user_ids:
            response = requests.get(
                f"https://api-v2.soundcloud.com/users/{user_id}/tracks?client_id={self._client_id}&limit={self._no_tracks_created}")
            if response.ok:
                jsondata += response.json()['collection']
        data = pd.DataFrame(jsondata)
        data.to_csv(path + '/created_tracks.csv', index=False)

    def get_data(self,  path='./data'):
        self._get_user_info(path)
        self._get_track_data(path)
        self._terminate()

    def _terminate(self):
        self._driver.close()
