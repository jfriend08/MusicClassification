import subprocess

for numDivide in xrange(2, 3):
  for k in xrange(100, 4000, 100):
    for batch in xrange(1, 6):
      for n_neighbors in xrange(6, 10):
        jobName = '{0}_{1}_{2}_{3}'.format(numDivide, k, batch / 10.0, n_neighbors)
        if k > 1000 and k < 2000:
          time = "10:00:00"
          ram = "6GB"
        elif k > 2000 and k < 3000:
          time = "100:00:00"
          ram = "11GB"
        elif k > 3000:
          time = "100:00:00"
          ram = "15GB"
        else:
          time = "7:00:00"
          ram = "5GB"

        l_cmd = "walltime=%s,mem=%s"%(time, ram)
        subprocess.call('qsub workPipeLine.pbs -N {0} -l {1} -v n={2},k={3},b={4},nei={5}'.format(jobName, l_cmd, numDivide, k, batch / 10.0, n_neighbors), shell=True)
