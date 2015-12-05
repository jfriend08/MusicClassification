import subprocess

for numDivide in xrange(1, 6):
  #for k in xrange(100, 4100, 100):
  for batch in xrange(1, 5):
    subprocess.call('qsub workPipeLine.pbs -v n={0},k={1},b={2}'.format(numDivide, 100, batch / 10.0), shell=True)
