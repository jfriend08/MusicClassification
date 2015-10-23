# Music Genre Classification
## Procedure
1. Download [GTZAN](http://marsyasweb.appspot.com/download/data_sets/) dataset
2. Pre-process data, including re-sampling and cliping
..*mv process.sh under genres and will auto perform pre-process
..So each music which all with 30s length will be trim for 10 clip, each clip is 3s, sampling rate is 22050 Hz
```bash
sox -r 22050 $j "$NAME"_clip1.au trim 0 3
sox -r 22050 $j "$NAME"_clip2.au trim 3 3
sox -r 22050 $j "$NAME"_clip3.au trim 6 3
...
```
3. Pre-processed data can be downloaded [here](https://onedrive.live.com/redir.aspx?cid=a134a87f7a3dd922&resid=A134A87F7A3DD922!347&parId=A134A87F7A3DD922!346&authkey=!ACiZA1wDdlb_fSk&ithint=file%2czip)