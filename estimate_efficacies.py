import numpy as np
import pandas as pd
from pathlib import Path
from june.records import RecordReader
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument(
    "-run",
    "--run",
    type=int,
    help="run number",
    default=0,
)

args = parser.parse_args()

data_dir = Path('/cosma6/data/dp004/dc-quer1/vaccine_paper_runs/efficacy_calibration_az/')

run = args.run
read = RecordReader(
    results_path=data_dir / f'results/run_{str(run).zfill(3)}/'
)
people_df = read.table_to_df('population')
infections_df = pd.read_csv(data_dir / f'results/run_{str(run).zfill(3)}/infections_df_{str(run).zfill(3)}.csv')
infections_df['timestamp'] = pd.to_datetime(infections_df['timestamp'])
infections_df.set_index('timestamp', inplace=True)
# exclude day of seed
infections_df = infections_df.loc['2021-06-27':]
infections_df.reset_index(inplace=True)
print(infections_df.head(3))
people_df = people_df[(people_df['age'] >= 18)]
infections_df = infections_df[infections_df['age'] >= 18]

n_by_vaccine_type = people_df.groupby(['vaccine_type']).size()

days_to_sample = 15
n_samples = ((infections_df['timestamp'].max() - infections_df['timestamp'].min())//days_to_sample).days - 1


date = infections_df['timestamp'].min() + datetime.timedelta(days=days_to_sample)
pfizer_efficacies = []
az_efficacies = []
dates = []
for i in range(n_samples):
    inf_df = infections_df[infections_df['timestamp'] <= date]
    percent_infected = inf_df.groupby(['vaccine_type']).size()/n_by_vaccine_type
    az_efficacies.append(1.-percent_infected.loc['astrazeneca']/percent_infected.loc['none'])
    pfizer_efficacies.append(1.-percent_infected.loc['pfizer']/percent_infected.loc['none'])

    dates.append(date)
    date += datetime.timedelta(days=days_to_sample)

az = pd.DataFrame(
    {'date': dates, 'AZ': az_efficacies}
)
az.set_index('date',inplace=True)
pfizer = pd.DataFrame(
    {'date': dates, 'Pfizer': pfizer_efficacies}
)
pfizer.set_index('date',inplace=True)

az.to_csv(f'/cosma7/data/dp004/dc-cues1/june_vaccines/az_az_run{run}.csv')
pfizer.to_csv(f'/cosma7/data/dp004/dc-cues1/june_vaccines/az_pfizer_run{run}.csv')
