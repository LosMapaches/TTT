import matplotlib.pyplot as pl
import pandas as pd
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
pl.savefig('propensity_for_motion.png')
pl.clf()
