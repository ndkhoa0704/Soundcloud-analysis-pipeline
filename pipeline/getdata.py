from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
import re
import numpy as np
import pandas as pd
import time
from datetime import date
import os


class SoundcloudCrawler:

    def __init__(
        self,
        userid_min: int,
        userid_max: int,
        no_users: int,
        no_tracks_liked: int,
        no_tracks_created: int,
        no_playlists_liked: int,
        no_playlists_created: int,
        checkpoint: bool,
        executable_path: str = None,
        data_path: str = '../data/raw'
    ):
        '''
        Use both api and html parser method to crawl data
        Parameters:
        * userid_min: lower-bound of user id number
        * userid_max: upper-bound of user id number
        * no_users: number of users to be crawled
        * no_tracks_liked: number of liked tracks to be crawled for each user
        * no_tracks_created: number of created tracks to be crawled for each user
        * no_playlists_created: number of created playlists to be crawled for each user
        * checkpoint: boolean indicates use of check point
        * executable_path: path to webdriver
        * data_path: path to folder to save data
        '''

        # Init variables
        self._WAITING_TIME = 0.05
        self._NUMBER_OF_ATTEMPTS = 3
        self._userid_max = userid_max
        self._userid_min = userid_min
        self._no_users = no_users
        self._data_path = data_path

        # Only used for forward and backward sampling
        self._checkpoint_path = './data/checkpoint'
        self._checkpoint = checkpoint

        self._no_tracks_liked = no_tracks_liked
        self._no_tracks_created = no_tracks_created
        self._no_playlists_liked = no_playlists_liked
        self._no_playlists_created = no_playlists_created
        self._userids = []
        self._cur_user_id = None

        # Create driver
        option = Options()
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        option.add_argument('--no-sandbox')

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
        while True:
            try:
                self._driver.get('https://soundcloud.com')
                log = self._driver.get_log('browser')
                client_id = re.search(
                    r"client_id=(.*?)\&", log[0]['message']).group(1)
            except:
                pass
            else:
                break
        return client_id

    def __sampling(self, count, sampling_method):
        if sampling_method == 'random':
            return np.random.randint(self._userid_min, self._userid_max + 1)
        elif sampling_method == 'forward':
            return count + 1
        elif sampling_method == 'backward':
            return count - 1
        else:
            raise Exception('Invalid argument')

    def _save_data(self, data, path):
        '''
        Update exists data files or save new ones
        '''
        today = date.today().strftime("%m-%d-%Y")
        if os.path.exists(path.format(today)):
            data.to_csv(path.format(today), mode='a',
                        index=False, escapechar='\\')
        else:
            data.to_csv(path.format(today), index=False, escapechar='\\')

    def _get_user_info(self, sampling_method: str):
        '''
        Get user data and store in user.csv
        '''
        jsondata = []
        print("GET USER INFO")

        # Load checkpoint
        if self._checkpoint:
            try:
                f = open(self._checkpoint_path, 'r')
                self._userid_min, self._userid_max = tuple(
                    map(int, f.read().split()))
            except:
                pass

        cur_id = self._userid_min
        for i in range(self._no_users):
            attempts = 0
            while True:
                attempts += 1
                cur_id = self.__sampling(cur_id, sampling_method)
                # This checking is used for random method
                if cur_id in self._userids:
                    continue

                user_id = cur_id
                got_user_in4 = False

                if user_id not in self._userids:
                    print(f'* Try: {user_id}, collected_users: {i}')
                    for j in range(self._NUMBER_OF_ATTEMPTS):
                        # Reset attemps since user id has not crawled yet
                        attempts = 0
                        time.sleep(self._WAITING_TIME)
                        print(f'Attempt {j + 1}')
                        response = None

                        try:
                            response = requests.get(
                                f'https://api-v2.soundcloud.com/users/{user_id}?client_id={self._client_id}')
                        except:
                            pass

                        if response and response.ok == True:
                            jsondata.append(response.json())
                            self._userids.append(user_id)
                            got_user_in4 = True
                            break
                # User info retrieved
                if got_user_in4 == True:
                    break

                # Stopping condition
                # Forward and backward
                if not self._userid_min <= cur_id <= self._userid_max:
                    break
                # Maximum attempts
            if not self._userid_min <= cur_id <= self._userid_max:
                break

        # Used as checkpoint
        self._cur_user_id = cur_id

        data = pd.json_normalize(jsondata)
        data['id'] = self._userids
        self._save_data(data, self._data_path + '/users-{}.csv')

    def _crawl(self, url, limit, msg):
        '''
        Only used for get tracks and playlists
        limit: number of items to be crawled
        '''
        jsondata = []
        count = 0
        for user_id in self._userids:
            print(f'* Task: {msg}, User id: {user_id}, user_number: {count}')
            count += 1
            for i in range(self._NUMBER_OF_ATTEMPTS):
                print(f'Attempt {i + 1}')
                time.sleep(self._WAITING_TIME)
                try:
                    response = requests.get(url.format(
                        user_id, self._client_id, limit))
                except:
                    pass
                if response and response.ok == True:
                    # Add user id
                    raw = response.json()['collection']
                    for i in raw:
                        i['userid'] = user_id
                    jsondata += raw
                    break
        return jsondata

    def _get_track_data(self):
        '''
        Get created tracks list
        Get liked tracks list
        '''

        # Crawl created tracks
        data = pd.json_normalize(self._crawl(
            'https://api-v2.soundcloud.com/users/{}/tracks?client_id={}&limit={}',
            self._no_tracks_created,
            "GET CREATED TRACKS DATA"
        ))

        # Save
        self._save_data(data, self._data_path + '/created_tracks-{}.csv')

        # Crawl liked tracks
        data = pd.json_normalize(self._crawl(
            'https://api-v2.soundcloud.com/users/{}/track_likes?client_id={}&limit={}',
            self._no_tracks_liked,
            "GET LIKED TRACKS DATA"
        ))

        # Save
        self._save_data(data, self._data_path + '/liked_tracks-{}.csv')

    def _get_playlist_data(self):
        '''
        Get liked playlists
        Get created playlists
        '''

        # Crawl created playlists
        data = pd.json_normalize(self._crawl(
            'https://api-v2.soundcloud.com/users/{}/playlists?client_id={}&limit={}',
            self._no_playlists_created,
            "GET CREATED PLAYLISTS DATA"
        ))

        # Save
        self._save_data(data, self._data_path + '/created_playlists-{}.csv')

        # Crawl liked playlists
        data = pd.json_normalize(self._crawl(
            'https://api-v2.soundcloud.com/users/{}/playlist_likes?client_id={}&limit={}',
            self._no_playlists_liked,
            "GET LIKED PLAYLISTS DATA"
        ))

        # Save
        self._save_data(data, self._data_path + '/liked_playlists-{}.csv')

    def get_data(self, sampling_method: str = 'forward'):
        '''
        Parameters:

        sampling_method: Decide how the user ids are chosen. Accepted values:
        * random: random sampling
        * forward: userid_min -> userid_max
        * backward: userid_max -> userid_min
        '''
        self._get_user_info(sampling_method)
        self._get_track_data()
        self._get_playlist_data()
        self._driver.close()

        # Update checkpoint
        if self._checkpoint:
            with open(self._checkpoint_path, 'w') as f:
                f.write(str(self._cur_user_id) + '\n')
                f.write(str(self._userid_max))
