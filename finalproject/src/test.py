import subprocess

for numDivide in xrange(1, 5):
  for k in xrange(5, 300, 5):
    for batch in xrange(1, 6):
      n_neighbors = 30
      jobName = '{0}_{1}_{2}_{3}_knnNewVLAD_flatten'.format(numDivide, k, batch / 10.0, n_neighbors)
      if k > 1000 and k < 2000:
        time = "20:00:00"
        ram = "7GB"
      elif k >= 2000 and k < 3000:
        time = "100:00:00"
        ram = "11GB"
      elif k >= 3000:
        time = "100:00:00"
        ram = "15GB"
      else:
        time = "20:00:00"
        ram = "5GB"

      l_cmd = "walltime=%s,mem=%s"%(time, ram)
      subprocess.call('qsub workPipeLine.pbs -N {0} -l {1} -v n={2},k={3},b={4},nei={5}'.format(jobName, l_cmd, numDivide, k, batch / 10.0, n_neighbors), shell=True)


# Gabriel
# for numDivide in xrange(1, 10):
#   for k in xrange(100, 4000, 100):
#     for batch in xrange(1, 3):
#       for n_neighbors in xrange(1, 30):

# for numDivide in xrange(1, 5):
#   for k in xrange(5, 200, 5):
#     for batch in xrange(1, 6):
#       n_neighbors = 10