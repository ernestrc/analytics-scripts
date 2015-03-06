from ggplot import *
import pandas

FILES = ['rich_dist_loopapp.csv', 'rich_dist_browser.csv']
AXISX = 'ct'
AXISY = 'perc'

def plot_distribution(df):
    plot = ggplot(df, aes(x=AXISX, y=AXISY, color='dimension')) + \
    geom_line() + \
    xlim(0,10) + \
    ggtitle('How does continued usage differ by loopType from 2014-08-04 to 2015-03-04') + \
    ylab('% Number of distinct guids') + \
    xlab('Number of connections')
    return plot

count = 0

for f in FILES:
    with open(f) as loaded:
        d = pandas.read_csv(loaded, sep='\t')
        if count == 0:
            df = d
        else:
            df = df.append(d)
        count += 1

plot_distribution(df)
