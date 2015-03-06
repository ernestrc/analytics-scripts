import subprocess
import csv
import json

# This script allows you to execute an arbitrary Hive query over every dimension found for
# a predefined dimension type (DIMENSION). The result of this queries will be outputed
# as a tab separated csv in the working directory.
#
# QUERY -> query to execute for every dimension found
# DIMENSIONS_QUERY -> query to get all the dimensions for the predefined type
#                     It should output only one column with a header.
# DIMENSION -> the dimension type
# DEBUG -> Set to True to execute as mysql
# TABLE -> Table where the queries will run against
#
# If debug mode is set, you will need to provide a config.json to set the mysql password

DIMENSION = 'sdk'
TABLE = 'LoopAppUserAgentIds'
DEBUG = True

def QUERY(dimension,value):
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
        return 'hive --hiveconf hive.cli.print.header=true --hiveconf hive.exec.parallel=true -e \"{}\" > {}'.format(query,outputFile)
    else:
        return 'mysql --user=root --password={} -e \"{}\" analytics > {}'.format(config["db-pass"], query, outputFile)

if __name__ == '__main__':
    if DEBUG:
        config = json.load(open('./config.json', 'rb'))
    else:
        config = {}
    dimensionsOut = './dimension-{}.csv'.format(DIMENSION)
    dim_cmd = queryInvoker(DIMENSIONS_QUERY(), dimensionsOut, config)
    subprocess.call(dim_cmd, shell=True)
    f = open(dimensionsOut)
    next(f)
    r = csv.reader(f, delimiter='\t')
    for row in r:
        if not row:
            row = None
        else:
            row = row[0].strip()
        outputFile = '{}-dimension-{}-output.csv'.format(DIMENSION,row)
        dist_cmd = queryInvoker(QUERY(DIMENSION,row), outputFile, config)
        subprocess.call(dist_cmd, shell=True)
