# OvercastAnalyse
Tools for analysing your overcast data.

**Creates plot of your played podcasts over time**

## Preperation

* login to [Overcast](https://overcast.fm/login) via Web (No account needed when using QR-Code)  
* download data under `Export Your Data` -> `All Data`

## Usage

`python3 PlayedDownloadHistory.py`

Default Values

`overcast.opml` is in project folder  
sum is made weekly (-d 7)

optional changes
```
-p PATH, --path PATH  path to overcast.opml file
-d DAYS, --days DAYS  days to be summed together for each dataPoint
```
