import matplotlib.pyplot as pl
import pandas as pd
import cPickle
import os

# Get the current directory and saved data analysis directory
first_directory = os.getcwd()
data_directory = first_directory+'/../data/analysis/'

# Change to data analysis directory
os.chdir(data_directory)


data = pd.read_csv(
                   'data_for_each_run_mean.txt',
                   sep=' ',
                   header=None
                   )

data.columns = ([
                 'temperature',
                 'temperature_std',
                 'distance',
                 'distance_std'
                 ])

pl.plot(
        data['temperature'],
        data['distance'],
        'b.'
        )

pl.xlabel('Temperature [K]')
pl.ylabel('Propensity for Motion [A^2]')
pl.grid(True)
pl.savefig('propensity_for_motion_temperature.png')
pl.clf()

with open('time.pkl', 'rb') as file:
    x = cPickle.load(file)

with open('dist.pkl', 'rb') as file:
    y = cPickle.load(file)

pl.figure()
runs = []
for key in x:
    x[key] = x[key] - x[key][0]  # Normalize
    pl.plot(x[key][:17], y[key][:17], '.')
    runs.append(key)

pl.xlabel('Step [-]')
pl.ylabel('Propensity for Motion <r^2> [A]')
pl.legend(runs)
pl.grid(True)
pl.savefig('propensity_for_motion_time.png')
pl.clf()
