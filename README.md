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
docker run -it soundcloud-pipeline bash
conda activate workenv
python -m main
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

# Collected data
* User info
* Created tracks
* Liked tracks
* Created playlists
* Liked playlists

# Important:
The project uses soundcloud api-v2, which is undocumented and can be easily changed in the future.