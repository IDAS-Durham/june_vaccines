import pandas as pd

def read_df(root='infections', run=0,):
    run_str= str(run).zfill(3)
    df = pd.read_csv(
        f'/cosma5/data/durham/covid19/arnau/runs/olympia_variations/results/run_{run_str}/{root}_df_{run_str}.csv'
    )
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    if root == 'infections':
        return df[df['location_specs'] != 'infection_seed']
    else:
        return df
