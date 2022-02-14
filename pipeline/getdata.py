from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
import re
import numpy as np
import pandas as pd
import time


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
        executable_path: str = None,
        data_path: str = '../data'
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
        * executable_path: path to webdriver
        * data_path: path to folder to save data
        '''

        # Init variables
        self._WAITING_TIME = 0.2
        self._NUMBER_OF_ATTEMPTS = 3
        self._userid_max = userid_max
        self._userid_min = userid_min
        self._no_users = no_users
        self._data_path = data_path
        self._no_tracks_liked = no_tracks_liked
        self._no_tracks_created = no_tracks_created
        self._no_playlists_liked = no_playlists_liked
        self._no_playlists_created = no_playlists_created
        self._userids = []

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

    def _get_user_info(self, sampling_method: str):
        '''
        Get user data and store in user.csv
        '''
        jsondata = []
        print("GET USER INFO")

        all_user_id = np.arange(
            start=self._userid_min, stop=self._userid_max, step=1)
        # Sampling
        if sampling_method == 'random':
            np.random.shuffle(all_user_id)
        elif sampling_method == 'forward':
            pass
        elif sampling_method == 'backward':
            all_user_id = all_user_id[::-1]
        else:
            raise Exception('Invalid argument')

        cur_idx = 0
        for i in range(self._no_users):
            '''
            Randomly choose a number between userid_min and userid_max
            Check for the id's validity and get user information
            Randoly pick a number that is used for user_id
            '''
            while True:
                user_id = all_user_id[cur_idx]
                cur_idx += 1
                got_user_in4 = False
                if user_id not in self._userids:
                    print(f'* Try: {user_id}, collected_users: {i}')
                    for j in range(self._NUMBER_OF_ATTEMPTS):
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
                # Stop the loop
                if got_user_in4 == True:
                    break

                # Stopping condition
                if cur_idx == all_user_id.shape[0]:
                    break
            if cur_idx == all_user_id.shape[0]:
                break
        print(len(self._userids))

        data = pd.json_normalize(jsondata)
        data['id'] = self._userids
        data.to_csv(self._data_path + '/user.csv', index=False)

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
                        i['id'] = user_id
                    jsondata += raw
                    break
        return jsondata

    def _get_track_data(self):
        '''
        Get created tracks list
        Get liked tracks list
        '''

        # Crawl created tracks
        data = pd.DataFrame(self._crawl(
            'https://api-v2.soundcloud.com/users/{}/tracks?client_id={}&limit={}',
            self._no_tracks_created,
            "GET CREATED TRACKS DATA"
        ))
        data.to_csv(self._data_path + '/created_tracks.csv', index=False, escapechar='\\')

        # Crawl liked tracks
        data = pd.DataFrame(self._crawl(
            'https://api-v2.soundcloud.com/users/{}/track_likes?client_id={}&limit={}',
            self._no_tracks_liked,
            "GET LIKED TRACKS DATA"

        ))
        data.to_csv(self._data_path + '/liked_tracks.csv', index=False, escapechar='\\')

    def _get_playlist_data(self):
        '''
        Get liked playlists
        Get created playlists
        '''

        # Crawl created playlists
        data = pd.DataFrame(self._crawl(
            'https://api-v2.soundcloud.com/users/{}/playlists?client_id={}&limit={}',
            self._no_playlists_created,
            "GET CREATED PLAYLISTS DATA"
        ))
        data.to_csv(self._data_path + '/created_playlist.csv',
                    index=False, escapechar='\\')

        # Crawl liked playlists
        data = pd.DataFrame(self._crawl(
            'https://api-v2.soundcloud.com/users/{}/playlist_likes?client_id={}&limit={}',
            self._no_playlists_liked,
            "GET LIKED TRACKS DATA"
        ))
        data.to_csv(self._data_path + '/liked_playlist.csv',
                    index=False, escapechar='\\')

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
