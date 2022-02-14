from pipeline.getdata import SoundcloudCrawler
from pipeline.preprocess import SoundcloudPreProcess

if __name__ == '__main__':
    crawler = SoundcloudCrawler(
        userid_min=1,
        userid_max=99999999,
        no_users=5000,
        no_tracks_liked=1000,
        no_tracks_created=1000,
        no_playlists_liked=1000,
        no_playlists_created=1000,
        executable_path='./chromedriver',
        data_path='./data'
    )
    crawler.get_data('forward')

    # preproc = SoundcloudPreProcess
