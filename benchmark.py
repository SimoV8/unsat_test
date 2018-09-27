import glob, os
import time
import subprocess
import re

specPro_path = '/home/simone/Tools/SpecPro/bin/SpecPro'
timeout = 600

for dir in ['Analisi2', 'Analisi3']:
    for i in range(10):
        for inputFile in glob.glob(dir + "/*/*.txt"):
            for m in ['linear', 'binary']:
                try:
                    start_time = time.time()
                    process = subprocess.Popen(specPro_path +' -i ' + inputFile + ' -timeout ' + str(timeout) + ' -m ' + m + ' -a ', shell=True, stdout=subprocess.PIPE)
                    process.wait(timeout)
                    end_time = time.time()

                    output = ""
                    for line in process.stdout:
                        output += line.decode('utf-8')

                    seed = re.search(r"seed: (\d+)", output)
                    mucSize = re.search(r"MUC of (\d+) elements found", output)

                    if seed != None and mucSize != None:
                        res = '%s, %s, %.5f, %s, %s' % (inputFile, m, end_time - start_time, mucSize.group(1), seed.group(1))
                    else:
                        print(output)
                        res = '%s, %s, %s' % (inputFile, m, 'FAIL')
                    print(res)
                    with open(dir + '/result.csv','a') as file:
                        file.write(res)
                        file.write('\n')
                    # print("time elapsed: %.5f seconds" % (end_time - start_time))
                    # print("MUC of %d elements found" % (nLines - 1))
                except subprocess.TimeoutExpired:
                    with open( dir + '/result.csv','a') as file:
                        res = '%s, %s, %s' % (inputFile, m, 'TIMEOUT')
                        file.write(res)
                        file.write('\n')
