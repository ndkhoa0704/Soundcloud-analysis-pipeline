from pipeline.getdata import Crawler

if __name__ == '__main__':
    crawler = Crawler(
        userid_min=1,
        userid_max=100,
        no_users=20,
        no_tracks_liked=500,
        no_tracks_created=500,
        executable_path='./chromedriver',
        data_path='./data'
    )
    crawler.get_data()
