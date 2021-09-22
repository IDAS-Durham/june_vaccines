import pandas as pd
from pathlib import Path

DATA_DIR = Path('/cosma6/data/dp004/dc-quer1/runs/queen/results/')

def read_df(root='infections', run=0,data_dir=DATA_DIR,):
    run_str= str(run).zfill(3)
    df = pd.read_csv(
        data_dir / f'run_{run_str}/{root}_df_{run_str}.csv'
    )
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('id',inplace=True)
    return df

def read_infections_and_deaths(run=0, data_dir=DATA_DIR):
    infections_df = read_df(run=run, data_dir=data_dir)
    deaths_df = read_df(run=run, root='deaths', data_dir=data_dir)
    if 'vaccine_type' in infections_df.columns:
        deaths_df['vaccine_type'] = infections_df.loc[deaths_df.index,'vaccine_type']
    infections_df = infections_df[infections_df['location_specs'] != 'infection_seed']
    return infections_df, deaths_df
