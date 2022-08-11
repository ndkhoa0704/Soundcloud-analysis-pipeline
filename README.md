# Soundcloud-analysis-pipeline
A simple pipeline to analyze soundcloud top tracks charts

---
# Usage
## Docker
```
docker build . -t soundcloud-pipeline
docker run -it -d soundcloud bash
conda activate workenv
```
**To get data generated from container:**
```
docker-compose up 
```

## Execution:

**Arguments**: 

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
    --clr create data file
**Run**
```
python -m main <arguments>
```

# Collected data
* User info
* Created tracks
* Liked tracks
* Created playlists
* Liked playlists