# Music Genre Classification Final Project
## Prolog
* Prepre data set under proper location, and change that location in workbook.py
* You can open workbook.ipynb to do local test and get familiar with the usage
* workbook.py is similiar to workbook.ipynb but with argparse for parameters
* n_mfcc = 20 is fixed
* The hyperplane we are going to test includes: # of clip, k, batch_size, # of neighbor


## Usage -- workbook.py
* numDivide - number of split of each clip. e.g. 3 then each clip will get 3 split, and you got 10*3=30 small clips for each song
* k - number of centroids
* batchSizeRatio - batch size ratio when finding centroids. If there are 100 point and you specify 0.1, then batch size will be 10
```
python workbook.py 3 4000 0.3 #numDivide, k, batchSizeRatio
```

## Usage -- workPipeLine.pbs
* You may change the `python workbook.py 3 4000 0.3` to the proper parameter you like to test
* Name the task according to the parameter setting `#PBS -N Run_3_4000_0.3`
* Current test: Run_3_4000_0.3 will get `Exit_status=271` and error is `job 7119487 exceeded MEM usage hard limit (6581 > 5120)`
```
qsub workPipeLine.pbs
```