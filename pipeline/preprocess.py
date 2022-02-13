import pandas as pd
import numpy as np

class SoundcloudPreProcess:
    '''
    A module to preprocess soundcloud raw data. Raw data should have csv format. Data to be processed:
    * User info
    * Created/Liked tracks
    * Created/Liked playlists
    Parameters:
    * userinfo_path: path to user info raw data
    * createdtracks_path: path to created tracks raw data
    * likedtracks_path: path to liked tracks raw data
    * createdplaylists_path: path to created playlists raw data
    * likedplaylists_path: path to liked playlists raw data
    * processed_path: path to processed data

    '''
    def __init__(
        self,
        userinfo_path,
        createdtracks_path,
        likedtracks_path,
        createdplaylists_path,
        likedplaylists_path,
        processed_path
    ):

        # Init variables
        self._userfinfo_path = userinfo_path
        self._createdtracks_path = createdtracks_path
        self._likedtracks_path = likedtracks_path
        self._createdplaylists_path = createdplaylists_path
        self._likedplaylists_path = likedplaylists_path
        self._processed_path = processed_path

    def _proc_userinfo(self):
        pass

    def _proc_tracks(self):
        pass
    
    def _proc_playlists(self):
        pass
        
    def process(self):
        pass

    