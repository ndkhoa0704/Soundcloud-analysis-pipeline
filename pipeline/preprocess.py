import pandas as pd
import os


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
        processed_path='./data/processed'
    ):

        # Init variables
        self._userfinfo_path = userinfo_path
        self._createdtracks_path = createdtracks_path
        self._likedtracks_path = likedtracks_path
        self._createdplaylists_path = createdplaylists_path
        self._likedplaylists_path = likedplaylists_path
        self._processed_path = processed_path

    def _proc_userinfo(self):
        '''
        Preprocess user info data
        '''
        data = pd.read_csv(self._userfinfo_path)

        data = data[[
            'city', 'comments_count', 'country_code', 'created_at',
            'followers_count', 'followings_count', 'id', 'kind', 'last_modified',
            'likes_count', 'playlist_likes_count', 'playlist_count',
            'reposts_count', 'track_count', 'verified', 'badges.pro',
            'badges.pro_unlimited', 'badges.verified'
        ]]

        data['created_at'] = pd.to_datetime(data['created_at'])
        data['last_modified'] = pd.to_datetime(data['last_modified'])

        # Save
        data.to_csv(self._processed_path + '/user.csv')

    def _proc_tracks(self):
        '''
        Preprocess created and liked tracks
        '''

        # Created tracks
        data = pd.read_csv(self._createdtracks_path)

        data = data[[
            'commentable', 'comment_count', 'created_at', 'description',
            'downloadable', 'download_count', 'duration', 'full_duration', 'genre',
            'last_modified', 'license', 'likes_count', 'playback_count',
            'public', 'release_date', 'reposts_count', 'state', 'streamable',
            'title', 'display_date', 'user.id'
        ]]

        # Convert string to datetime object
        data['created_at'] = pd.to_datetime(data['created_at'])
        data['release_date'] = pd.to_datetime(data['release_date'])
        data['display_date'] = pd.to_datetime(data['display_date'])

        data.to_csv(self._processed_path + '/created_tracks.csv')

        # Liked tracks
        data = pd.read_csv(self._likedtracks_path)

        data = data[[
            'created_at', 'userid', 'track.comment_count', 'track.created_at',
            'track.downloadable', 'track.download_count', 'track.duration',
            'track.full_duration', 'track.genre', 'track.id', 'track.last_modified',
            'track.license', 'track.likes_count', 'track.playback_count',
            'track.release_date', 'track.reposts_count', 'track.state',
            'track.title', 'track.user_id', 'track.display_date', 'track.user.id',
            'track.user.username', 'track.user.verified', 'track.user.city',
            'track.user.country_code', 'track.user.badges.pro',
            'track.user.badges.pro_unlimited', 'track.user.badges.verified'
        ]]

        data['created_at'] = pd.to_datetime(data['created_at'])
        data['track.created_at'] = pd.to_datetime(data['track.created_at'])
        data['track.last_modified'] = pd.to_datetime(
            data['track.last_modified'])
        data['track.release_date'] = pd.to_datetime(data['track.release_date'])
        data['track.display_date'] = pd.to_datetime(data['track.display_date'])

        data.to_csv(self._processed_path + '/liked_tracks.csv')

    def _proc_playlists(self):
        '''
        Preprocess created and liked playlists
        '''

        # Created playlists
        data = pd.read_csv(self._createdplaylists_path)

        data = data[[
            'created_at', 'duration', 'genre', 'id', 'last_modified', 'license',
            'likes_count', 'release_date', 'reposts_count', 'title', 'user_id',
            'published_at', 'display_date'
        ]]

        data['created_at'] = pd.to_datetime(data['created_at'])
        data['last_modified'] = pd.to_datetime(data['last_modified'])
        data['release_date'] = pd.to_datetime(data['release_date'])
        data['published_at'] = pd.to_datetime(data['published_at'])
        data['display_date'] = pd.to_datetime(data['display_date'])

        # Save
        data.to_csv(self._processed_path + '/created_playlists.csv')

        # Liked playlists
        data = data[[
            'created_at', 'id', 'playlist.created_at', 'playlist.duration',
            'playlist.id', 'playlist.last_modified', 'playlist.likes_count',
            'playlist.reposts_count', 'playlist.title', 'playlist.track_count',
            'playlist.user_id', 'playlist.published_at', 'playlist.release_date',
            'playlist.display_date', 'playlist.user.followers_count',
            'playlist.user.id', 'playlist.user.username', 'playlist.user.verified',
            'playlist.user.city', 'playlist.user.country_code',
            'playlist.user.badges.pro', 'playlist.user.badges.pro_unlimited',
            'playlist.user.badges.verified'
        ]]

        data['created_at'] = pd.to_datetime(data['created_at'])
        data['playlist.created_at'] = pd.to_datetime(
            data['playlist.created_at'])
        data['playlist.last_modified'] = pd.to_datetime(
            data['playlist.last_modified'])
        data['playlist.published_at'] = pd.to_datetime(
            data['playlist.published_at'])
        data['playlist.release_date'] = pd.to_datetime(
            data['playlist.release_date'])
        data['playlist.display_date'] = pd.to_datetime(
            data['playlist.display_date'])

        data.to_csv(self._processed_path + '/liked_playlists.csv')

    def process(self):
        self._proc_userinfo()
        self._proc_tracks()
        self._proc_playlists()
