import pandas
import ast
from scipy.interpolate import interp1d
import pickle


def parse_sec_loc(sec_loc):
    return ast.literal_eval(sec_loc)

EPSPNORM = 0.5
df = pandas.read_csv('grid_search.csv')[['config/sec', 'config/weight', 'epsp']]
df.rename(columns={'config/sec': 'sec', 'config/weight': 'weight'}, inplace=True)

secs = df['sec'].unique()

weight_norms = {}

for sec in secs:

    
# for each section calculate the weight where the epsp at soma == 0.5
    entries = df[df['sec'] == sec].sort_values(by='weight')
    #print(entries)
    weights = entries['weight']
    epsps = entries['epsp']
    f = interp1d(epsps, weights, fill_value='extrapolate')
    #print([*zip(weights, epsps)])
    weight_norm = f(EPSPNORM) / EPSPNORM
    weight_norms[sec] = [weight_norm]


with open('weight_norms.pkl', 'wb') as fptr:
    pickle.dump(weight_norms, fptr)
