# Soundcloud-analysis-pipeline
[![.github/workflows/pipelinejob.yml](https://github.com/ndkhoa0704/Soundcloud-analysis-pipeline/actions/workflows/pipelinejob.yml/badge.svg)](https://github.com/ndkhoa0704/Soundcloud-analysis-pipeline/actions/workflows/pipelinejob.yml)

A simple pipeline that does:
* Data collection 
* Preprocess data
* Analyze and generate report

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
docker cp <CONTAINER's NAME/ID>:<data path in the container> <data path on host>
```

## Ubuntu
**Dependencies:**
* chromedriver
* google chrome or chromium web browser
* selenium 4.1.0
* sklearn
* beautifulsoup 4.10.0
* numpy
* pandas
* requests 2.27.1


### Conda
```
conda env create -n environment.yml
```

### Python venv
```
pip install -r requirements.txt
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

# Important:
The project uses soundcloud api-v2, which is undocumented and can be easily changed in the future.
