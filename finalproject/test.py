import subprocess

for numDivide in xrange(1, 2):
  for k in xrange(100, 4000, 100):
    for batch in xrange(1, 6):
      for n_neighbors in xrange(1, 6):
        jobName = '{0}_{1}_{2}_{3}'.format(numDivide, k, batch / 10.0, n_neighbors)
        subprocess.call('qsub workPipeLine.pbs -N {0} -v n={1},k={2},b={3},nei={4}'.format(jobName, numDivide, k, batch / 10.0, n_neighbors), shell=True)
