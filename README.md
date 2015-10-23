# Music Genre Classification
## Procedure
1. Download [GTZAN](http://marsyasweb.appspot.com/download/data_sets/) dataset
2. Pre-process data, including re-sampling and cliping
..*mv process.sh under genres and will auto perform the following pre-process
```bash
sox -r 22050 $j "$NAME"_clip1.au trim 0 3
sox -r 22050 $j "$NAME"_clip2.au trim 3 3
sox -r 22050 $j "$NAME"_clip3.au trim 6 3
sox -r 22050 $j "$NAME"_clip4.au trim 9 3
sox -r 22050 $j "$NAME"_clip5.au trim 12 3
sox -r 22050 $j "$NAME"_clip6.au trim 15 3
sox -r 22050 $j "$NAME"_clip7.au trim 18 3
sox -r 22050 $j "$NAME"_clip8.au trim 21 3
sox -r 22050 $j "$NAME"_clip9.au trim 24 3
sox -r 22050 $j "$NAME"_clip10.au trim 27 3
```
