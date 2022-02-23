from pipeline.getdata import SoundcloudCrawler
from pipeline.preprocess import SoundcloudPreprocess
import sys
import getopt

if __name__ == '__main__':

    '''
    Arguments: 
    -r <userid_min:userid_max> (default: 1:999999999)
    --nu <number of users> (default: 1000)
    --nr <number of records for each users> (default: 1000)
    --ep <driver path> (default: ./chromedriver)
    --rdp <rdata path> (default: ./data/raw)
    --nct <number of created tracks> (default: 1000)
    --nlt <number of liked tracks> (default: 1000)
    --ncp <number of created playlists> (default: 1000)
    --nlp <number of liked playlists> (default: 1000)
    --pdp <processed data path> (default: ./data/processed)
    -m <sampling method> (default: random)
    -c used to continue crawling from last user id (forward and backward)
    '''

    # Argument parsings
    optlist, _ = getopt.getopt(
        sys.argv[1:],
        '-r:m:c',
        ['nu=', 'nr=', 'ep=', 'rdp=', 'nct=', 'nlt=', 'ncp=', 'nlp=', 'pdp=']
    )

    # Init variables
    no_users = 1000
    no_records = no_created_tracks = no_liked_tracks = \
        no_created_playlists = noliked_playlist = 1000
    executable_path = './chromedriver'
    raw_data_path = './data/raw'
    processed_data_path = './data/processed'
    id_range = [1, 999999999]
    checkpoint = False
    method = 'random'

    # Parse arguments
    for opt, arg in optlist:
        if opt == '--nr':
            no_created_tracks = no_liked_tracks = \
                no_created_playlists = noliked_playlist = arg
        elif opt == '-r':
            id_range = list(map(int, arg.split(':')))
        elif opt == '--nu':
            no_users = int(arg)
        elif opt == '--nct':
            no_created_tracks = int(arg)
        elif opt == '--nlt':
            no_liked_tracks = int(arg)
        elif opt == '--ncp':
            no_created_playlists = int(arg)
        elif opt == '--nlp':
            noliked_playlist = int(arg)
        elif opt == '--pdp':
            processed_data_path = arg
        elif opt == '--rdp':
            raw_data_path = arg
        elif opt == '-m':
            method = arg
        elif opt == '--ep':
            executable_path = arg
        elif opt == '-c':
            checkpoint = True
        else:
            raise Exception('Bad arguments')

    # Further checkings
    if method == 'random' and checkpoint == True:
        raise Exception('checkpoint does not work with random method')

    # Crawl data
    crawler = SoundcloudCrawler(
        userid_min=id_range[0],
        userid_max=id_range[1],
        no_users=no_users,
        no_tracks_liked=no_liked_tracks,
        no_tracks_created=no_created_tracks,
        no_playlists_liked=no_liked_tracks,
        no_playlists_created=no_created_playlists,
        executable_path=executable_path,
        data_path=raw_data_path,
        checkpoint=checkpoint
    )

    crawler.get_data(method)

    # Preprocess
    preproc = SoundcloudPreprocess(raw_data_path, processed_data_path)

    preproc.process()
