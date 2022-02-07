from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
import re
import json
import random
import pandas as pd

class soundcloud_crawler:
    def __init__(self, executable_path=None):
        # Use both api and html parser method to crawl data 
        option = Options()
        service = Service(executable_path)
        option.add_argument('headless', 'disable-gpu')
        if executable_path:
            self.driver = Chrome(executable_path=executable_path, options=option)
        else:
            self.driver = Chrome(service=service, options=option)
        
    
    def _get_client_id(self):
        # Use selenium to get client id
        # Get client id of the logged-in user in the browser
        self.driver.get('https://soundcloud.com')
        log = self.driver.get_log('browser')
        for i in log:
            client_id = re.search(r'client_id=(.*?)\&', i)
        return client_id
    
    def get_data(self, estimated_no_users, min_user_id, max_user_id, path='../data'):
        client_id = self._get_client_id()
        user_ids = random.sample(range(min_user_id,max_user_id + 1),estimated_no_users)
        data = pd.DataFrame('')
        for user_id in user_ids:
            user_ids.append(random.randint(min_user_id, max_user_id))
            response = requests.get(f"https://api-v2.soundcloud.com/users/{user_id}/tracks?client_id={client_id}")
            if response.ok:
                response.json()['collection']





        