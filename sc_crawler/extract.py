from getdata import SC_crawler
import sys
import getopt

if __name__ == '__main__':

    '''
    Arguments: 
    -r <userid_min:userid_max> (default: 1:999999999)
    --nu <number of users> (default: 1000)
    --nr <number of records for each users> (default: 1000)
    --dr <driver path> (default: ./chromedriver)
    --nct <number of created tracks> (default: 1000)
    --nlt <number of liked tracks> (default: 1000)
    --ncp <number of created playlists> (default: 1000)
    --nlp <number of liked playlists> (default: 1000)
    -m <sampling method> (default: random)
    '''

    # Argument parsings
    optlist, _ = getopt.getopt(
        sys.argv[1:],
        '-r:m:c',
        ['nu=', 'nr=', 'dr=', 'nct=',
            'nlt=', 'ncp=', 'nlp=']
    )

    # Init variables
    no_users = 50
    no_records = no_created_tracks = no_liked_tracks = \
        no_created_playlists = noliked_playlist = 10000
    driver_path = './chromedriver'
    id_range = [1, 999999999]
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
        elif opt == '-m':
            method = arg
        elif opt == '--dr':
            executable_path = arg
        else:
            raise Exception('Bad arguments')

    # Crawl data
    crawler = SC_crawler(
        userid_min=id_range[0],
        userid_max=id_range[1],
        no_users=no_users,
        no_tracks_liked=no_liked_tracks,
        no_tracks_created=no_created_tracks,
        no_playlists_liked=no_liked_tracks,
        no_playlists_created=no_created_playlists,
        driver_path=driver_path,
        dbname='scpipe',
        conn_str='mongodb://scpipe_mongo:27017'
    )

    crawler.collect()
