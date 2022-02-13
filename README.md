# Soundcloud-analysis-pipeline
A simple pipeline that does:
* Data collection 
* Preprocess data
* Analyzing and generate report

---
# Usage
## Docker
```
docker build . -t soundcloud-pipeline
docker run -it -d soundcloud bash
conda activate workenv
python -m main
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

**Execution:**
```
python -m main
```
## Conda
```
conda env create -n environment.yml
```

## Python venv
```
pip install -r requirements.txt
```



# Collected data
* User info
* Created tracks
* Liked tracks
* Created playlists
* Liked playlists

# Important:
The project uses soundcloud api-v2, which is undocumented and can be easily changed in the future.