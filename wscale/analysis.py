import pandas
import ast
from scipy.interpolate import interp1d
import pickle
import logging

logging.basicConfig(filename='analysis.log', level=logging.INFO,
                    format='%(levelname)s:%(message)s')

#def parse_sec_loc(sec_loc): # OLDER VERSION REQUIRED SEC_LOC
#    return ast.literal_eval(sec_loc) # NOW USING NEW SESSION.REPORT W/ SEC, LOC

EPSPNORM = 0.5
df = pandas.read_csv('wscale_search.csv')
#sec_locs = df['config/sec_loc'].apply(parse_sec_loc)
#df[['sec', 'loc']] = pandas.DataFrame(sec_locs.tolist(), index=df.index)
secs = df['sec'].unique()
logging.info("Number of trials: %d", len(df))
logging.info("Number of sections: %d", len(secs))
logging.info("Weight array: %s", df['weight'].unique())
wnorms = {}
for sec in secs:
    locs = df[df['sec'] == sec]['loc'].unique()
    locs.sort()
    logging.info("processing section %s with %d locations", sec, len(locs))
    wnorms[sec] = []
    for loc in locs:
    # for each section calculate the weight where the epsp at soma == 0.5
        entries = df[df['sec'] == sec].sort_values(by='weight')
    #print(entries)
        weights = entries['weight']
        epsps = entries['epsp']
        f = interp1d(epsps, weights, fill_value='extrapolate')
    #print([*zip(weights, epsps)])
        wnorm = f(EPSPNORM) / EPSPNORM
        wnorms[sec].append(wnorm)
        logging.info('%s(%.2f): wscale = %.6f', sec, loc, wnorm)

with open('weight_norms.pkl', 'wb') as f:
    pickle.dump(wnorms, f)



