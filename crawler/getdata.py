from bleach import clean
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import re
import pandas as pd
import time
from bs4 import BeautifulSoup
import pymongo


class SCcrawl:
    # Crawl data and saved in json format
    # Get top 100 musics
    # Based on the top chart musics, crawl creators
    # Crawl each creator liked tracks, created tracks ,liked playlists, created playlists
    def __init__(
        self,
        connection_string: str = None,
        executable_path: str = None
):

        # Init variables
        self._NUMBER_OF_ATTEMPTS = 10
        self._WAITING_TIME = 0.03
        self._top_chart_user = None
        self._records_limit = 100

        # MongoDB database
        # Get MongoDB database
        client = pymongo.MongoClient(connection_string)
        self._database =  client['SoundCloud']

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

    def _get_genres(self):
        for _ in range(self._NUMBER_OF_ATTEMPTS):
            time.sleep(self._WAITING_TIME)
            try:
                self._driver.get(
                    "https://soundcloud.com/charts/top?genre=all-music&country=all-countries")
                WebDriverWait(self._driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/div/div/div[1]/div[3]/div/div[4]/ul/li[1]/div/div[1]')))
                soup = BeautifulSoup(self._driver.page_source, features="html.parser")
                genres_raw = soup.findAll("span",class_="sc-button-label-alt")
                # Remove tags about current genres from the sample page
                genres_raw.pop(0)
                genres_raw.pop(0)
                genres = []
                for genre_r in genres_raw:
                    genre = genre_r.string
                    genre = re.sub('[^A-Za-z0-9]+', '', genre).lower()
                    genres.append(genre)
                genres[0] = 'all-music'
                genres[1] = 'all-audio'
            except TimeoutException:
                continue
            else:
                break
        return genres

    def _get_top_chart(self, client_id):
        top_user = dict()
        genres = self._get_genres()
        jsondata = []
        # Get top 100 music for each genre
        for g in genres:
            #####
            # Test
            print(f'Current genre: {g}')
            #####

            time.sleep(self._WAITING_TIME)

            for _ in range(self._NUMBER_OF_ATTEMPTS):
                response = requests.get(
                    f'''
                    https://api-v2.soundcloud.com/charts?kind=top&genre=soundcloud%3Agenres%3A{g}&offset=0&limit=100&client_id={client_id}&app_version=1461312517
                    ''')
                if response.ok == True:
                    break
            data = response.json()
            jsondata.append(data)
            # Get list of users' ids
            top_user[g] = pd.json_normalize(data['collection'])['track.user.id']
        
        self._top_chart_user = top_user

        # Save
        self._database['top_chart'].insert_many(jsondata)

    def _get_client_id(self):
        # Use selenium to get client id
        # Get client id of the logged-in user in the browser
        for _ in range(self._NUMBER_OF_ATTEMPTS):
            time.sleep(self._WAITING_TIME)
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

    def _get_user_info(self, client_id):
        '''
        Get user data
        '''
        self._get_genres()
        genres = list(self._top_chart_user.keys())
        for g in genres:
            print(f'Current genre: {g}')
            jsondata = []
            time.sleep(self._WAITING_TIME)
            for user_id in self._top_chart_user[g]:
                print(f'Current user id: {user_id}')
                for _ in range(self._NUMBER_OF_ATTEMPTS):

                    response = None
                    time.sleep(self._WAITING_TIME)

                    try:
                        response = requests.get(
                            f'https://api-v2.soundcloud.com/users/{user_id}?client_id={client_id}')
                    except:
                        pass
                    
                    if response and response.ok == True:
                        # Get tracks and playlists data of each user
                        data = response.json()
                        data['created_tracks'], data['liked_tracks'] = self._get_track_data(user_id, client_id) 
                        data['created_playlists'], data['liked_playlists'] = self._get_playlist_data(user_id, client_id) 
                        jsondata.append(data)
                        break
                    
            # Save data
            self._database[f'top-{g}-users'].insert_many(jsondata)

    def _crawl(self, url):
        '''
        Only used for get tracks and playlists
        limit: number of items to be crawled
        '''
        jsondata = []
        for _ in range(self._NUMBER_OF_ATTEMPTS):
            time.sleep(self._WAITING_TIME)
            try:
                response = requests.get(url)
            except:
                pass
            if response and response.ok == True:
                break
        return jsondata

    def _get_track_data(self, user_id, client_id):
        '''
        Get created tracks list
        Get liked tracks list
        '''

        # Crawl created tracks
        created_tracks = self._crawl(
            f'https://api-v2.soundcloud.com/users/{user_id}/tracks?client_id={client_id}&limit={self._records_limit}',
        )

        # Crawl liked tracks
        liked_tracks = self._crawl(
            f'https://api-v2.soundcloud.com/users/{user_id}/track_likes?client_id={client_id}&limit={self._records_limit}',
        )

        return created_tracks, liked_tracks


    def _get_playlist_data(self, user_id, client_id):
        '''
        Get liked playlists
        Get created playlists
        '''

        # Crawl created playlists
        created_playlists = self._crawl(
            f'https://api-v2.soundcloud.com/users/{user_id}/playlists?client_id={client_id}&limit={self._records_limit}',
        )

        # Crawl liked playlists
        liked_playlists = self._crawl(
            f'https://api-v2.soundcloud.com/users/{user_id}/playlist_likes?client_id={client_id}&limit={self._records_limit}',
        )
        
        return created_playlists, liked_playlists

    def get_data(self, waiting_time=None):
        '''
        Parameters:

        sampling_method: Decide how the user ids are chosen. Accepted values:
        * random: random sampling
        * forward: userid_min -> userid_max
        * backward: userid_max -> userid_min
        waiting_time: amount of time needed between records (None: default 0.03)
        '''
        if waiting_time != None:
            self._WAITING_TIME = waiting_time
        
        client_id = self._get_client_id()
        self._get_top_chart(client_id)
        self._get_user_info(client_id)
        del client_id


if __name__ == '__main__':

    crawler = SCcrawl(
        connection_string="mongodb://localhost:27017/",
        executable_path='./chromedriver'
        )
    
    crawler.get_data(0.3)