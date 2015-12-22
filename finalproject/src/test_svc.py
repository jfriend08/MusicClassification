import subprocess
import numpy as np

job = 's48'

for numDivide in xrange(1,5):
  for k in xrange(5, 200, 5):
    for batch in xrange(3, 5):
      C = 2
      jobName = '{0}_{1}_{2}_{3}_svcNewVLAD200wWhitenScatterHPMFCC'.format(numDivide, k, batch / 10.0, C)
      # print jobName
      if k > 1000 and k < 2000:
        time = "20:00:00"
        ram = "9GB"
      elif k >= 2000 and k < 3000:
        time = "100:00:00"
        ram = "11GB"
      elif k >= 3000:
        time = "100:00:00"
        ram = "15GB"
      else:
        time = "20:00:00"
        ram = "7GB"

      l_cmd = "walltime=%s,mem=%s"%(time, ram)
      subprocess.call('qsub workPipeLine_svcNewVLAD.pbs -N {0} -q {1} -l {2} -v n={3},k={4},b={5},C={6}'.format(
        jobName, job, l_cmd, numDivide, k, batch / 10.0, C), shell=True)

# for numDivide in xrange(1,5):
#   for k in xrange(5, 1000, 10):
#     for batch in xrange(1, 5):
# for numDivide in xrange(5, 15):
#   for k in xrange(100, 2000, 500):
#     for batch in xrange(1, 2):
#       for C in np.arange(0.0001, 1, 0.05):
#         jobName = '{0}_{1}_{2}_{3}_svc'.format(numDivide, k, batch / 10.0, C)
#         # print jobName
#         if k > 1000 and k < 2000:
#           time = "10:00:00"
#           ram = "7GB"
#         elif k >= 2000 and k < 3000:
#           time = "100:00:00"
#           ram = "11GB"
#         elif k >= 3000:
#           time = "100:00:00"
#           ram = "15GB"
#         else:
#           time = "7:00:00"
#           ram = "5GB"

#         l_cmd = "walltime=%s,mem=%s"%(time, ram)
#         subprocess.call('qsub workPipeLine_svc.pbs -N {0} -q {1} -l {2} -v n={3},k={4},b={5},C={6}'.format(
#           jobName, job, l_cmd, numDivide, k, batch / 10.0, C), shell=True)
