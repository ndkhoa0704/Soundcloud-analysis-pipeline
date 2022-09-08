from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
import re
import numpy as np
import time
import datetime as dt
from collector.collector import Collector

# UTC format
CURRENT_TIME_STR = dt.datetime.utcnow().isoformat()[:-7] + 'Z'


class SC_crawler(Collector):

    def __init__(
        self,
        userid_min: int,
        userid_max: int,
        no_users: int,
        no_tracks_liked: int,
        no_tracks_created: int,
        no_playlists_liked: int,
        no_playlists_created: int,
        driver_path: str = None,
        **kwargs
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
        * driver_path: path to webdriver
        * data_path: path to folder to save data
        '''

        super().__init__(**kwargs)

        # Init variables
        self._WAITING_TIME = None
        self._NUMBER_OF_ATTEMPTS = 5
        self._MAX_SKIP_USER = 1000
        self._userid_max = userid_max
        self._userid_min = userid_min
        self._no_users = no_users

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
        if driver_path:
            self._driver = Chrome(service=Service(
                driver_path), options=option)
        else:
            self._driver = Chrome(options=option)

        # Get client id
        self._client_id = self._get_client_id()

    def _save_data(self, collname: str, data: list):
        '''
        Save data to mongodb

        # Parameters:
        - collname: collection name
        - data: list of json data

        # Return:
        - None
        '''
        if data == None:
            return False
        
        collection = self._db.get_collection(collname)
        collection.insert_many(data)
        return True

    def _get_client_id(self):
        '''
        Get soundcloud client's id from with chrome
        # Return
        - client_id: str
        '''
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

    def _get_user_info(self, sampling_method: str):
        '''
        Get user data and store in user.csv
        '''
        jsondata = []
        cur_id = self._userid_min
        cur_try_get_user = 0
        for _ in range(self._no_users):
 
            # Stop if a certain amount of user ids are skipped 
            if cur_try_get_user == self._MAX_SKIP_USER:
                raise 'Possible server error or we are banned from server'

            while True:
                cur_id = self.__sampling(cur_id, sampling_method)
                user_id = cur_id
                got_user_in4 = False
                if user_id not in self._userids:
                    for _ in range(self._NUMBER_OF_ATTEMPTS):
                        time.sleep(self._WAITING_TIME)
                        response = None

                        try:
                            response = requests.get(
                                f'https://api-v2.soundcloud.com/users/{user_id}?client_id={self._client_id}')
                        except:
                            pass

                        # Log
                        # print('Current user: ', user_id)

                        if response and response.ok == True:
                            # Add date
                            data = response.json()
                            data['get_date'] = CURRENT_TIME_STR
                            jsondata.append(data)
                            self._userids.append(user_id)
                            got_user_in4 = True
                            break
                # User info retrieved
                if got_user_in4 == True:
                    cur_try_get_user = 0
                    break
                else:
                    cur_try_get_user += 1

                # Stopping condition
                # Forward and backward
                if not self._userid_min <= cur_id <= self._userid_max:
                    break
                # Maximum attempts
            if not self._userid_min <= cur_id <= self._userid_max:
                break

        # Save
        self._save_data('users', jsondata)

    def _crawl(self, url, limit):
        '''
        Only used for get tracks and playlists
        limit: number of items to be crawled
        '''
        jsondata = []
        for user_id in self._userids:
            for _ in range(self._NUMBER_OF_ATTEMPTS):
                time.sleep(self._WAITING_TIME)
                try:
                    response = requests.get(url.format(
                        user_id, self._client_id, limit))
                except:
                    pass
                if response and response.ok == True:
                    # Add user id
                    data = response.json()
                    data['get_date'] = CURRENT_TIME_STR
                    data['userid'] = user_id
                    jsondata.append(data)
                    break

        if len(jsondata) == 0:
            return None
            
        return jsondata

    def _get_track_data(self):
        '''
        Get created tracks list
        Get liked tracks list
        '''

        # Crawl created tracks
        data = self._crawl(
            'https://api-v2.soundcloud.com/users/{}/tracks?client_id={}&limit={}',
            self._no_tracks_created
        )

        # Save
        self._save_data('created_tracks', data)

        # Crawl liked tracks
        data = self._crawl(
            'https://api-v2.soundcloud.com/users/{}/track_likes?client_id={}&limit={}',
            self._no_tracks_liked
        )

        # Save
        self._save_data('liked_tracks', data)

    def _get_playlist_data(self):
        '''
        Get liked playlists
        Get created playlists
        '''

        # Crawl created playlists
        data = self._crawl(
            'https://api-v2.soundcloud.com/users/{}/playlists?client_id={}&limit={}',
            self._no_playlists_created
        )

        # Save
        self._save_data('created_playlists', data)

        # Crawl liked playlists
        data = self._crawl(
            'https://api-v2.soundcloud.com/users/{}/playlist_likes?client_id={}&limit={}',
            self._no_playlists_liked
        )

        # Save
        self._save_data('liked_playlists', data)

    def collect(self, waiting_time=0.03, sampling_method: str = 'random'):
        '''
        Parameters:

        sampling_method: Decide how the user ids are chosen. Accepted values:
        * random: random sampling
        * forward: userid_min -> userid_max
        * backward: userid_max -> userid_min
        waiting_time: amount of time needed between records (None: default 0.03)
        '''

        self._WAITING_TIME = waiting_time

        self._get_user_info(sampling_method)
        self._get_track_data()
        self._get_playlist_data()
        self._driver.close()
