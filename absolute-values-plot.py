import pandas as pd
import matplotlib.pyplot as plt
import numpy


import sys
import csv


def running_mean(x, N):
    cumsum = numpy.cumsum(numpy.insert(x.values, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

try:
    filename_opcode = str(sys.argv[1])
    filename_kv_u = str(sys.argv[2])
    filename_kv_c = str(sys.argv[3])
    fromblock = int(sys.argv[4])
    toblock = int(sys.argv[5])
except:
    print "usage: python absolute-values-plot.py <filename_opcode> <filename_kv_uncompressed> <filename_kv_compressed> <fromblock> <toblock>"
    exit(1)

series = {}
with open(filename_opcode, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        line_count += 1

        if int(row['BlockNumber']) < fromblock:
            continue
        for k, v in row.iteritems():
            k = k + "_opcode"

            if not k in series:
                series[k] = []

            series[k].append(int(v))
        if int(row['BlockNumber']) > toblock:
            break

        if line_count % 100000 == 0:
            print "1/3 processed opcode", line_count, "rows"

with open(filename_kv_u, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        line_count += 1

        if int(row['BlockNumber']) < fromblock:
            continue

        for k, v in row.iteritems():
            k = k + "_kv_u"

            if not k in series:
                series[k] = []

            series[k].append(int(v))
        if int(row['BlockNumber']) > toblock:
            break

        if line_count % 100000 == 0:
            print "2/3 processed kv(uncompressed)", line_count, "rows"

with open(filename_kv_c, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        line_count += 1

        if int(row['BlockNumber']) < fromblock:
            continue

        for k, v in row.iteritems():
            k = k + "_kv_c"

            if not k in series:
                series[k] = []

            series[k].append(int(v))
        if int(row['BlockNumber']) > toblock:
            break

        if line_count % 100000 == 0:
            print "3/3 processed kv(compressed)", line_count, "rows"


df = pd.DataFrame(series)
print df

plt.ylabel("MB")
plt.xlabel("block #")
plt.grid(True)

running_mean_size = 1024


plt.plot(
    df['BlockNumber_opcode'].values[running_mean_size-1:],
    running_mean(df['BlockWitnessSize_opcode']/1024.0/1024.0, running_mean_size),
    label = "opcode witness")

plt.plot(
    df['BlockNumber_kv_u'].values[running_mean_size-1:],
    running_mean(df['BlockWitnessSize_kv_u']/1024.0/1024.0, running_mean_size),
    label = "kv witness (uncompressed)")

plt.plot(
    df['BlockNumber_kv_c'].values[running_mean_size-1:],
    running_mean(df['BlockWitnessSize_kv_c']/1024.0/1024.0, running_mean_size),
    label = "kv witness (compressed)")


plt.legend()


plt.show()
