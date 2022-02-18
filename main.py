from pipeline.getdata import SoundcloudCrawler
from pipeline.preprocess import SoundcloudPreProcess
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
    '''

    # Argument parsings
    optlist, _ = getopt.getopt(
        sys.argv[1:],
        '-r:m:',
        ['nu=', 'nr=', 'ep=', 'rdp=', 'nct=', 'nlt=', 'ncp=', 'nlp=', 'pdp=']
    )

    # Init variables
    nu = 1000
    nr = nct = nlt = ncp = nlp = 1000
    ep = './chromedriver'
    rdp = './data/raw'
    pdp = './data/processed'
    r = [1, 999999999]
    method = 'random'

    # Parse arguments
    for opt, arg in optlist:
        if opt == '--nr':
            nct = nlt = ncp = nlt = arg
        elif opt == '-r':
            r = list(map(int, arg.split(':')))
        elif opt == '--nu':
            nu = int(arg)
        elif opt == '--nct':
            nct = int(arg)
        elif opt == '--nlt':
            nlt = int(arg)
        elif opt == '--ncp':
            ncp = int(arg)
        elif opt == '--nlp':
            nlp = int(arg)
        elif opt == '--pdp':
            pdp = arg
        elif opt == '--rdp':
            rdp = arg
        elif opt == '-m':
            method = arg
        else:
            raise Exception('Bad arguments')

    # Crawl data
    crawler = SoundcloudCrawler(
        userid_min=r[0],
        userid_max=r[1],
        no_users=nu,
        no_tracks_liked=nlt,
        no_tracks_created=nct,
        no_playlists_liked=nlp,
        no_playlists_created=ncp,
        executable_path=ep,
        data_path=rdp
    )

    crawler.get_data(method)

    # Preprocess
    preproc = SoundcloudPreProcess(rdp, pdp)

    preproc.process()
