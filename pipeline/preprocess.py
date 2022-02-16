import pandas as pd


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
        processed_path='../data/processed'
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

        data.drop(columns=[
            'avatar_url', 'description', 'creator_subscriptions', 'full_name',
            'last_name', 'first_name', 'groups_count', 'permalink', 'last_modified',
            'permalink_url', 'uri', 'urn', 'username',  'station_urn',
            'station_permalink', 'creator_subscription.product.id', 'visuals.urn',
            'visuals.enabled', 'visuals.visuals', 'visuals.tracking', 'visuals'
        ], inplace=True)

        data['created_date'] = pd.to_datetime(data['created_date'])
        data['last_modified'] = pd.to_datetime(data['last_modified'])

        # Save
        data.to_csv(self._processed_path + '/user.csv')

    def _proc_tracks(self):
        '''
        Preprocess created and liked tracks
        '''

        # Created tracks
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

        # Convert string to datetime object
        data['created_at'] = pd.to_datetime(data['created_at'])
        data['release_date'] = pd.to_datetime(data['release_date'])
        data['display_date'] = pd.to_datetime(data['display_date'])

        data.to_csv(self._processed_path + '/created_tracks.csv')

        # Liked tracks
        data = pd.read_csv(self._likedtracks_path)

        data.drop(columns=[
            'kind', 'track.artwork_url', 'track.caption',
            'track.commentable', 'track.description', 'track.embeddable_by',
            'track.has_downloads_left', 'track.kind',
            'track.label_name', 'track.permalink', 'track.permalink_url',
            'track.public', 'track.publisher_metadata.id',
            'track.publisher_metadata.urn', 'track.publisher_metadata.contains_music',
            'track.purchase_title', 'track.purchase_url', 'track.secret_token',
            'track.sharing', 'track.streamable', 'track.tag_list',
            'track.track_format', 'track.uri', 'track.urn',
            'track.visuals', 'track.waveform_url',
            'track.media.transcodings', 'track.station_urn',
            'track.station_permalink', 'track.track_authorization',
            'track.monetization_model', 'track.policy', 'track.user.avatar_url',
            'track.user.first_name', 'track.user.followers_count',
            'track.user.full_name', 'track.user.kind',
            'track.user.last_modified', 'track.user.last_name',
            'track.user.permalink', 'track.user.permalink_url', 'track.user.uri',
            'track.user.urn', 'track.user.station_urn', 'track.user.station_permalink',
            'track.publisher_metadata.artist', 'track.publisher_metadata.album_title',
            'track.publisher_metadata.upc_or_ean', 'track.publisher_metadata.isrc',
            'track.publisher_metadata.explicit', 'track.publisher_metadata.p_line',
            'track.publisher_metadata.p_line_for_display',
            'track.publisher_metadata.c_line',
            'track.publisher_metadata.c_line_for_display',
            'track.publisher_metadata.writer_composer',
            'track.publisher_metadata.release_title',
            'track.publisher_metadata.publisher', 'track.publisher_metadata',
            'track.publisher_metadata.iswc', 'track.visuals.urn',
            'track.visuals.enabled', 'track.visuals.visuals',
            'track.visuals.tracking', 'track.visuals.tracking.impression'
        ], inplace=True)

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
        data.drop(columns=[
            'artwork_url', 'description', 'embeddable_by',
            'kind', 'label_name',
            'managed_by_feeds', 'permalink', 'permalink_url',
            'public', 'purchase_title', 'purchase_url',
            'secret_token', 'sharing', 'tag_list', 'uri',
            'set_type', 'is_album', 'track_count', 'user.avatar_url', 'user.first_name',
            'user.followers_count', 'user.full_name', 'user.id', 'user.kind',
            'user.last_modified', 'user.last_name', 'user.permalink',
            'user.permalink_url', 'user.uri', 'user.urn', 'user.username',
            'user.verified', 'user.city', 'user.country_code', 'user.badges.pro',
            'user.badges.pro_unlimited', 'user.badges.verified', 'user.station_urn',
            'user.station_permalink'
        ])

        data['created_at'] = pd.to_datetime(data['created_at'])
        data['last_modified'] = pd.to_datetime(data['last_modified'])
        data['release_date'] = pd.to_datetime(data['release_date'])
        data['published_at'] = pd.to_datetime(data['published_at'])
        data['display_date'] = pd.to_datetime(data['display_date'])

        # Save
        data.to_csv(self._processed_path + '/created_playlists.csv')

        # Liked playlists
        data.drop(columns=[
            'kind',
            'playlist.managed_by_feeds', 'playlist.permalink',
            'playlist.permalink_url', 'playlist.public',
            'playlist.secret_token', 'playlist.sharing', 'playlist.user.kind',
            'playlist.uri', 'playlist.set_type', 'playlist.kind',
            'playlist.is_album', 'playlist.artwork_url',
            'playlist.user.avatar_url', 'playlist.user.first_name',
            'playlist.user.full_name', 'playlist.user.last_modified',
            'playlist.user.last_name', 'playlist.user.permalink',
            'playlist.user.permalink_url', 'playlist.user.uri', 'playlist.user.urn',
            'playlist.user.station_urn', 'playlist.user.station_permalink'
        ], inplace=True)

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
