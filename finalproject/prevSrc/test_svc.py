import subprocess
import numpy as np

for numDivide in xrange(1, 2):
  for k in xrange(100, 4000, 100):
    for batch in xrange(1, 2):
      for C in np.arange(0.0001, 1, 1):
        jobName = '{0}_{1}_{2}_{3}_svc'.format(numDivide, k, batch / 10.0, C)
        # print jobName
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
        subprocess.call('qsub workPipeLine_svc.pbs -N {0} -l {1} -v n={2},k={3},b={4},C={5}'.format(jobName, l_cmd, numDivide, k, batch / 10.0, C), shell=True)
