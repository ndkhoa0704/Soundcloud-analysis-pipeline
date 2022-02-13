from pipeline.getdata import Crawler

if __name__ == '__main__':
    crawler = Crawler(
        userid_min=1,
        userid_max=99999999,
        no_users=1000,
        no_tracks_liked=100,
        no_tracks_created=100,
        no_playlists_liked=100,
        no_playlists_created=100,
        executable_path='./chromedriver',
        data_path='./data'
    )
    crawler.get_data()
