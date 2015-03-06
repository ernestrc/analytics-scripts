import csv
import pandas
import sys

FILE_IN = sys.argv[1]
OBS_COL_IDX = int(sys.argv[2])
OBS_COL_NAME = sys.argv[3]

observations = 0

with open(FILE_IN) as f:
    c = csv.reader(f)
    next(c)
    for row in c:
        observations += int(row[OBS_COL_IDX])

df = pandas.read_csv(FILE_IN)

df['perc'] = df[OBS_COL_NAME].div(observations)

print 'Total observations {}'.format(observations)

df.to_csv('rich_' + FILE_IN)
