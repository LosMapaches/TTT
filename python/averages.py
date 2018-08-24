from matplotlib import pyplot as pl
from analysis import analize as an

import pandas as pd
import numpy as np
import setup
import os

# Directories
first_directory = os.getcwd()
data_directory = first_directory+'/../data/'
dump_directory = data_directory+'analysis/msd/'

# Grab file names from the lammpstrj directory
names = os.listdir(data_directory+'lammpstrj/')

# Grab the run names
count = 0
for item in names:
    names[count] = item.split('.lammpstrj')[0]
    count += 1


def eim(msd, mean_msd):
    ''' Take the error in the mean.'''

    # Save the number of columns and rows
    rows, columns = msd.shape

    # Subtract each MSD at every time from the average and square it
    out = []
    for i in range(rows):
        value = np.subtract(msd[i], mean_msd)
        value **= 2
        out.append(value)

    # Get STD for each timepoint
    std_msd = (np.sum(out, axis=0)/rows)**0.5

    # Get error in the mean for each timepoint
    eim_msd = std_msd/(rows**0.5)

    # Return the error in the mean
    return eim_msd


def avg(*args, **kwargs):
    '''
    Do analysis for every run.
    '''

    series = args[0]

    print('Analyzing all '+series+' runs')

    # Grab names that match the series input
    newnames = []
    for item in names:
        if series in item and series[0] == item[0]:
            newnames.append(item)

    # Gather plots, vibration, and MSD data for each run
    msd = []
    data = {}
    fcc = []
    hcp = []
    bcc = []
    ico = []
    for name in newnames:
        run = an(name, *args[1:], **kwargs)
        run.rdf()

        clusters = run.neighbor()
        fcc.append(clusters['FCC'])
        hcp.append(clusters['HCP'])
        bcc.append(clusters['BCC'])
        ico.append(clusters['ICO'])


        value_msd = run.msd()
        msd.append(value_msd[1])

        for key in value_msd[2]:
            if data.get(key) is None:
                data[key] = []
            data[key].append(value_msd[2][key])

        # Try to generate graphs from txt file if available
        try:
            run.response()
        except Exception:
            pass

    # Step data from last iteration on previous loop
    time = value_msd[0]

    print('Taking the mean data for ' + series)

    # Take the mean row by row for each atom for MSD
    msd = np.array(msd)
    mean_msd = np.mean(msd, axis=0)

    # Get error in the mean for each timepoint
    eim_msd = eim(msd, mean_msd)

    # Get the mean MSD for atom types and EIM
    data_mean = {}
    eim_data = {}

    # Control the frequency of errorbars
    errorfreq = len(time)//10

    for key in data:
        data[key] = np.array(data[key])
        data_mean[key] = np.mean(data[key], axis=0)
        eim_data[key] = eim(data[key], data_mean[key])
        pl.errorbar(
                    time,
                    data_mean[key],
                    eim_data[key],
                    errorevery=errorfreq,
                    label='Element Type: %i' % key
                    )

    # Plot the mean MSD
    pl.errorbar(
                time,
                mean_msd,
                eim_msd,
                errorevery=errorfreq,
                label='Total MSD'
                )

    pl.xlabel('Time [ps]')
    pl.ylabel('MSD Averaged [A^2]')
    pl.legend()
    pl.grid(b=True, which='both')
    pl.tight_layout()
    pl.savefig('../images/motion/'+series+'_avgMSD')
    pl.clf()

    msdcolumns = [time, mean_msd, eim_msd]

    order = list(data_mean.keys())
    order.sort()

    # Grab data for MSD and EIM
    for item in order:
        msdcolumns.append(data_mean[item])
        msdcolumns.append(eim_data[item])

    # Save data in alternating oder of MSD and EIM (first is time)
    output = dump_directory+series+'_msd_average.txt'
    np.savetxt(output, np.transpose(msdcolumns))

    # Average the number of clusters accross runs
    fccavg = np.mean(fcc)
    hcpavg = np.mean(hcp)
    bccavg = np.mean(bcc)
    icoavg = np.mean(ico)

    clusters = [fccavg, hcpavg, bccavg, icoavg]

    # The labels for clusters in the xlabel
    labels = ['FCC', 'HCP', 'BCC', 'ICO']
    location = [1, 2, 3, 4]

    count = 0
    for v, i in enumerate(clusters):
        pl.text(
                v+1, i,
                ' '+str(clusters[count]),
                color='red',
                ha='center',
                fontweight='bold'
                )

        count += 1

    pl.bar(location, clusters,  align='center')
    pl.xticks(location, labels)
    pl.xlabel('Cluster [-]')
    pl.ylabel('[count/ps]')
    pl.grid(b=True, which='both')
    pl.tight_layout()
    pl.savefig('../images/neighbor/'+series+'_avgneighbor')
    pl.clf()

    # Return the steps with their corresponding msd mean
    return time, mean_msd, eim_msd, data_mean, eim_data
