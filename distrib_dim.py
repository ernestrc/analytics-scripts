import subprocess
import csv
import json

DIMENSION = 'sdk'
TABLE = 'LoopAppUserAgentIds'
DEBUG = True

def DISTRIBUTION_QUERY(dimension,value):
    return '''
        select ct, count(*) obs, {} as dimension from (
            select count(distinct connection_id) ct, {}, guid
            from LoopAppUserAgentIds
            group by guid, {}
        ) tt
        where {}='{}'
        group by ct, {}
    '''.format(dimension, dimension, dimension, dimension, value, dimension)

def DIMENSIONS_QUERY():
    return 'select distinct {} from {}'.format(DIMENSION, TABLE)

def queryInvoker(query, outputFile, config):
    if not DEBUG:
        return 'hv -e \"{}\" > {}'.format(query,outputFile)
    else:
        return 'mysql --user=root --password={} -e \"{}\" analytics > {}'.format(config["db-pass"], query, outputFile)

if __name__ == '__main__':
    config = json.load(open('./config.json', 'rb'))
    dimensionsOut = './dimension-{}.csv'.format(DIMENSION)
    dim_cmd = queryInvoker(DIMENSIONS_QUERY(), dimensionsOut, config)
    subprocess.call(dim_cmd, shell=True)
    f = open(dimensionsOut)
    next(f) #skip header
    r = csv.reader(f, delimiter='\t')
    for row in r:
        if not row:
            row = None
        else:
            row = row[0].strip()
        outputFile = '{}-{}-distrib.csv'.format(DIMENSION,row)
        dist_cmd = queryInvoker(DISTRIBUTION_QUERY(DIMENSION,row), outputFile, config)
        subprocess.call(dist_cmd, shell=True)
