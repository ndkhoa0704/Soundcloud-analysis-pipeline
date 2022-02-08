from pipeline.getdata import Crawler

if __name__ == '__main__':
    crawler = Crawler(1, 100, 20)
    crawler.get_data()
