# Music Genre Classification
## Procedure
* Download [GTZAN](http://marsyasweb.appspot.com/download/data_sets/) dataset
* Pre-process data, including re-sampling and cliping
* mv process.sh under genres and will auto perform pre-process. So each music which all with 30s length will be trim for 10 clip, each clip is 3s, sampling rate is 22050 Hz
```bash
sox -r 22050 $j "$NAME"_clip1.au trim 0 3
sox -r 22050 $j "$NAME"_clip2.au trim 3 3
sox -r 22050 $j "$NAME"_clip3.au trim 6 3
...
```
* Pre-processed data can be downloaded [HERE](https://onedrive.live.com/redir.aspx?cid=a134a87f7a3dd922&resid=A134A87F7A3DD922!347&parId=A134A87F7A3DD922!346&authkey=!ACiZA1wDdlb_fSk&ithint=file%2czip)

## Materialize data
* Need scipy installed
* pythonize.py needs to be in the same directory of `genres_processed`

## Mel Filter Bank
* Package is downloaded [HERE](https://github.com/SiggiGue/pyfilterbank)
* Make sure numpy is imported in hpc environment, and make sure ssh -X into hpc
```
module load python/intel/2.7.6
```
* Run
```
python signalScattering.py
```
* You will see figures generated
![alt text](https://github.com/jfriend08/MusicClassification/blob/dev/figures/Mel_Matrix.png "Mel_Matrix")
![alt text](https://github.com/jfriend08/MusicClassification/blob/dev/figures/mel_frequency_bank.png "mel_frequency_bank")
* Low-pass filter (order of 6) will be designed by scipy.signal.butter, and filtered by scipy.signal.lfilter.
![alt text](https://github.com/jfriend08/MusicClassification/blob/dev/figures/lowPassButterFilter.png "lowPassButterFilter")
* Low-pass filter (order of 6) will be designed by scipy.signal.butter, and filtered by scipy.signal.lfilter. Here is an example of on of classical clip being filtered by 50Hz low-pass
![alt text](https://github.com/jfriend08/MusicClassification/blob/dev/figures/FilterFigure_classical.png "FilterFigure_classical")