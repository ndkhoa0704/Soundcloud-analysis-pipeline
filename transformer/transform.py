import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date


class SCviz:
    TODAY = date.today().strftime("%m-%d-%Y")

    def __init__(
        self,
        raw_path='./data/raw',
        processed_path='./data/processed'
    ):
        '''
        A module to preprocess soundcloud raw data. Raw data should have csv format. Data to be processed:
        * User info (user.csv)
        * Created and liked tracks (created_tracks.csv and liked_tracks.csv)
        * Created and liked playlists (created_playlists.csv and liked_playlists.csv)
        Parameters:
        * raw_path: path to folder that contains raw data
        '''
        # Init variables
        self._raw_path = raw_path
        self._processed_path = processed_path

    def _proc_userinfo(self):
        '''
        Preprocess user info data
        '''
        data = pd.read_csv(self._raw_path + f'/users-{self.TODAY}.csv')

        data = data[[
            'city', 'comments_count', 'country_code', 'created_at',
            'followers_count', 'followings_count', 'id', 'last_modified',
            'likes_count', 'playlist_likes_count', 'playlist_count',
            'reposts_count', 'track_count', 'verified', 'badges.pro',
            'badges.pro_unlimited', 'badges.verified', 'username'
        ]]

        data['country_code'] = data['country_code'].fillna('Other')
        data['created_at'] = pd.to_datetime(
            data['created_at'], errors='coerce')
        data['last_modified'] = pd.to_datetime(
            data['last_modified'], errors='coerce')

        return data

    def _proc_created_tracks(self):
        '''
        Preprocess created tracks
        '''

        data = pd.read_csv(self._raw_path + f'/created_tracks-{self.TODAY}.csv')

        data = data[[
            'id', 'userid', 'commentable', 'comment_count', 'created_at',
            'downloadable', 'download_count', 'duration',
            'full_duration', 'genre', 'last_modified', 'license',
            'likes_count', 'playback_count', 'public', 'release_date',
            'reposts_count', 'state', 'streamable', 'title', 'display_date',
        ]]

        # Convert string to datetime object
        data['created_at'] = pd.to_datetime(
            data['created_at'], errors='coerce')
        data['release_date'] = pd.to_datetime(
            data['release_date'], errors='coerce')
        data['display_date'] = pd.to_datetime(
            data['display_date'], errors='coerce')
        return data

    def _proc_liked_tracks(self):
        '''
        Preprocess liked tracks
        '''

        data = pd.read_csv(self._raw_path + f'/liked_tracks-{self.TODAY}.csv')
        data = data[[
            'created_at', 'userid', 'track.comment_count', 'track.created_at',
            'track.downloadable', 'track.download_count', 'track.duration',
            'track.full_duration', 'track.genre', 'track.id', 'track.last_modified',
            'track.license', 'track.likes_count', 'track.playback_count',
            'track.release_date', 'track.reposts_count', 'track.state',
            'track.title', 'track.user_id', 'track.display_date', 'track.user.id',
            'track.user.username', 'track.user.verified', 'track.user.city',
            'track.user.country_code', 'track.user.badges.pro',
            'track.user.badges.pro_unlimited', 'track.user.badges.verified',
            'track.commentable'
        ]]

        # Time conversion
        data['created_at'] = pd.to_datetime(data['created_at'])
        data['track.created_at'] = pd.to_datetime(
            data['track.created_at'], errors='coerce')
        data['track.last_modified'] = pd.to_datetime(
            data['track.last_modified'], errors='coerce')
        data['track.release_date'] = pd.to_datetime(
            data['track.release_date'], errors='coerce')
        data['track.display_date'] = pd.to_datetime(
            data['track.display_date'], errors='coerce')

        return data

    def _proc_created_playlists(self):
        '''
        Preprocess created playlists
        '''

        data = pd.read_csv(
            self._raw_path + f'/created_playlists-{self.TODAY}.csv')

        data = data[[
            'userid', 'created_at', 'duration', 'genre', 'id', 'last_modified',
            'license', 'likes_count', 'release_date', 'reposts_count', 'title',
            'published_at', 'display_date', 'track_count'
        ]]

        data['created_at'] = pd.to_datetime(
            data['created_at'], errors='coerce')
        data['last_modified'] = pd.to_datetime(
            data['last_modified'], errors='coerce')
        data['release_date'] = pd.to_datetime(
            data['release_date'], errors='coerce')
        data['published_at'] = pd.to_datetime(
            data['published_at'], errors='coerce')
        data['display_date'] = pd.to_datetime(
            data['display_date'], errors='coerce')

        return data

    def _proc_liked_playlists(self):
        '''
        Preprocess liked playlists
        '''

        data = pd.read_csv(self._raw_path + f'/liked_playlists-{self.TODAY}.csv')

        data = data[[
            'userid', 'created_at', 'playlist.created_at', 'playlist.duration',
            'playlist.id', 'playlist.last_modified', 'playlist.likes_count',
            'playlist.reposts_count', 'playlist.title', 'playlist.track_count',
            'playlist.published_at', 'playlist.release_date', 'playlist.display_date',
            'playlist.user.followers_count', 'playlist.user.username', 'playlist.user.verified',
            'playlist.user.city', 'playlist.user.country_code',
            'playlist.user.badges.pro', 'playlist.user.badges.pro_unlimited',
            'playlist.user.badges.verified'
        ]]

        # Time conversion
        data['created_at'] = pd.to_datetime(
            data['created_at'], errors='coerce')
        data['playlist.created_at'] = pd.to_datetime(
            data['playlist.created_at'], errors='coerce')
        data['playlist.last_modified'] = pd.to_datetime(
            data['playlist.last_modified'], errors='coerce')
        data['playlist.published_at'] = pd.to_datetime(
            data['playlist.published_at'], errors='coerce')
        data['playlist.release_date'] = pd.to_datetime(
            data['playlist.release_date'], errors='coerce')
        data['playlist.display_date'] = pd.to_datetime(
            data['playlist.display_date'], errors='coerce')

        return data

    def _preprocess(self):
        self._proc_userinfo()
        self._proc_created_tracks()
        self._proc_liked_tracks()
        self._proc_created_playlists()
        self._proc_liked_playlists()
