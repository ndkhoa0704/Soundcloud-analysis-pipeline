import pandas as pd
import numpy as np
import ast

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
        '''
        Preprocess user info data
        '''
        data = pd.read_csv(self._userfinfo_path)

        # Drop columns
        data.drop(columns=[
            'avatar_url', 'description', 'creator_subscriptions','full_name', 
            'last_name', 'first_name', 'groups_count', 'permalink', 
            'permalink_url', 'uri', 'urn', 'username',  'station_urn', 
            'station_permalink', 'creator_subscription.product.id', 'visuals.urn', 
            'visuals.enabled', 'visuals.visuals', 'visuals.tracking','visuals'
        ], inplace=True)

        # Convert string to datetime object
        data['created_date'] = pd.to_datetime(data['created_date'])
        data['last_modified'] = pd.to_datetime(data['last_modified'])    

    def _proc_tracks(self):
        
        data = pd.read_csv(self._createdtracks_path)
        data.drop(columns=[
            'artwork_url', 'caption', 'embeddable_by', 'kind', 'label_name', 'permalink', 
            'permalink_url', 'publisher_metadata', 'purchase_title', 'purchase_url', 
            'secret_token', 'sharing', 'tag_list', 'track_format', 'uri', 'urn',
            'visuals', 'waveform_url', 'station_urn', 'station_permalink',
            'track_authorization', 'monetization_model', 'policy', 'media.transcodings',
            'user.avatar_url', 'user.first_name', 'user.followers_count', 'user.full_name',
            'user.kind', 'user.last_modified', 'user.last_name', 'user.permalink',
            'user.permalink_url', 'user.uri', 'user.urn', 'user.username',
            'user.verified', 'user.city', 'user.country_code', 'user.badges.pro',
            'user.badges.pro_unlimited', 'user.badges.verified', 'user.station_urn', 'user.station_permalink',
            'publisher_metadata.id', 'publisher_metadata.urn', 'publisher_metadata.contains_music', 
            'publisher_metadata.artist', 'publisher_metadata.album_title', 'publisher_metadata.publisher', 
            'publisher_metadata.isrc', 'publisher_metadata.writer_composer', 'publisher_metadata.upc_or_ean', 
            'publisher_metadata.explicit', 'publisher_metadata.c_line', 'publisher_metadata.c_line_for_display',
            'publisher_metadata.release_title', 'publisher_metadata.iswc', 'has_downloads_left', 
            'publisher_metadata.p_line', 'publisher_metadata.p_line_for_display'
        ], inplace=True)

        data['created_at'] = pd.to_datetime(data['created_at'])
        data['release_date'] = pd.to_datetime(data['release_date'])
        data['display_date'] = pd.to_datetime(data['display_date'])
    
    def _proc_playlists(self):
        pass
        
    def process(self):
        pass

    
