from ggplot import *
import pandas
import os

DATA_FOLDER = './data'
AXISX = 'ct'
AXISY = 'perc'
DIMENSION = 'country'
GROUP = 'dimension'
TITLE = 'How does continued usage differ by {} from 2014-08-04 to 2015-03-04'.format(DIMENSION)
YLABEL = '% Number of distinct guids'
XLABEL = 'Number of connections'
XLIMIT = 10

def plot_lines(df, axisx, axisy, group, title, yl, xl, lim):
    plot = ggplot(df, aes(x=axisx, y=axisy, color=group)) + \
        geom_line() + \
        xlim(0, lim) + \
        ggtitle(title) + \
        ylab(yl) + \
        xlab(xl)
    return plot

# Merges all csv files in the given folder into a single df
def mergeDataFrames(data_folder):
    files = []
    for filename in os.listdir(data_folder):
        fullPath = data_folder+'/'+filename
        if os.path.getsize(fullPath) > 0 and 'dimensions' not in filename:
            print 'Merging ' + filename
            files.append(fullPath)

    count = 0

    for f in files:
        with open(f) as loaded:
            d = pandas.read_csv(loaded, sep='\t')
            if count == 0:
                df = d
            else:
                df = df.append(d)
            count += 1
    return df

if __name__ == '__main__':
    df = mergeDataFrames(DATA_FOLDER)
    plot_lines(df, AXISX, AXISY, GROUP, TITLE, YLABEL, XLABEL, XLIMIT)
