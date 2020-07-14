import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import sys
import csv

adjust_keys = False
try:
    filename_opcode = str(sys.argv[1])
    filename_kv_u = str(sys.argv[2])
    filename_kv_c = str(sys.argv[3])
    fromblock = int(sys.argv[4])
    toblock = int(sys.argv[5])
except:
    print "usage: python percentile.py <filename_opcode> <filename_kv_uncompressed> <filename_kv_compressed> <fromblock> <toblock>"
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

            if adjust_keys:
                if k == 'LeafKeysSize_hex':
                    v = int(v) / 2
                if k == 'BlockWitnessSize_hex':
                    leafKeySizeOriginal = int(row['LeafKeysSize'])
                    leafKeySizeAdjusted = int(leafKeySizeOriginal / 2)
                    v = int(v) - leafKeySizeOriginal + leafKeySizeAdjusted

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
            k = k + "_kv_uncompressed"

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
            k = k + "_kv_compressed"

            if not k in series:
                series[k] = []

            series[k].append(int(v))
        if int(row['BlockNumber']) > toblock:
            break

        if line_count % 100000 == 0:
            print "3/3 processed kv (compressed)", line_count, "rows"



df = pd.DataFrame(series)
print df

print 'opcode'
print "mean", df['BlockWitnessSize_opcode'].mean()
print "median", df['BlockWitnessSize_opcode'].median()
print "percentile 90th", df['BlockWitnessSize_opcode'].quantile(0.9)
print "percentile 95th", df['BlockWitnessSize_opcode'].quantile(0.95)
print "percentile 99th", df['BlockWitnessSize_opcode'].quantile(0.99)
print "percentile 100th", df['BlockWitnessSize_opcode'].quantile(1.0)

print 'kv_compressed'
print "mean", df['BlockWitnessSize_kv_compressed'].mean()
print "median", df['BlockWitnessSize_kv_compressed'].median()
print "percentile 90th", df['BlockWitnessSize_kv_compressed'].quantile(0.9)
print "percentile 95th", df['BlockWitnessSize_kv_compressed'].quantile(0.95)
print "percentile 99th", df['BlockWitnessSize_kv_compressed'].quantile(0.99)
print "percentile 100th", df['BlockWitnessSize_kv_compressed'].quantile(1.0)


print 'kv_uncompressed'
print "mean", df['BlockWitnessSize_kv_uncompressed'].mean()
print "median", df['BlockWitnessSize_kv_uncompressed'].median()
print "percentile 90th", df['BlockWitnessSize_kv_uncompressed'].quantile(0.9)
print "percentile 95th", df['BlockWitnessSize_kv_uncompressed'].quantile(0.95)
print "percentile 99th", df['BlockWitnessSize_kv_uncompressed'].quantile(0.99)
print "percentile 100th", df['BlockWitnessSize_kv_uncompressed'].quantile(1.0)



plt.xlabel("MB")

plt.boxplot((df['BlockWitnessSize_opcode']/1024.0/1024.0,df['BlockWitnessSize_kv_compressed']/1024.0/1024.0, df['BlockWitnessSize_kv_uncompressed']/1024.0/1024.0,), vert=False, labels=["opcode", "kv(compressed)","kv(uncompressed)"], showfliers=False, whis=[1,99])

plt.show()
