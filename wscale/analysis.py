import pandas
from scipy.interpolate import interp1d

EPSPNORM = 0.5
df = pandas.read_csv('grid_search.csv')[['config/sec', 'config/weight', 'epsp']]
secs = df['config/sec'].unique()

for sec in secs:
# for each section calculate the weight where the epsp at soma == 0.5
    entries = df[df['config/sec'] == sec].sort_values(by='config/weight')
    #print(entries)
    weights = entries['config/weight']
    epsps = entries['epsp']
    f = interp1d(epsps, weights, fill_value='extrapolate')
    #print([*zip(weights, epsps)])
    wnorm = f(EPSPNORM) / EPSPNORM
