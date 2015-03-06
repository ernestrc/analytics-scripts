import csv
import pandas
import sys
import os

DATA_FOLDER = './data'
OBSERVATIONS_COLUMN = 'obs'

def enrich(fe, column):
    df = pandas.read_csv(fe, delimiter='\t')
    observations = df[column].sum()
    df['perc'] = df[column].div(observations)
    print 'Total observations {}'.format(observations)
    df.to_csv(fe, sep='\t')

def enrichFiles(folderPath, column):
    for filename in os.listdir(folderPath):
        enrich(folderPath+'/'+filename, column)

if __name__ == '__main__':
    enrichFiles(DATA_FOLDER, OBSERVATIONS_COLUMN)
