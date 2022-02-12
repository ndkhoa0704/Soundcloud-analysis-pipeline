from pipeline.getdata import Crawler

if __name__ == '__main__':
    crawler = Crawler(
        userid_min=1,
        userid_max=99999999,
        no_users=5000,
        no_tracks_liked=5000,
        no_tracks_created=5000,
        no_playlists_liked=5000,
        no_playlists_created=5000,
        executable_path='chromedriver',
        data_path='./data'
    )
    crawler.get_data()
