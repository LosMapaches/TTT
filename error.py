from matplotlib import pyplot as pl
from scipy import stats as st

from diffusionimport import loaddiffusions as load
from matplotlib import lines
from itertools import islice

from ukuiestimator import error as ukui
from batchmeans import error as batch

import numpy as np
import os

regular, multiple, order = load('../export/')

# Apply methods to Multiple Origins
temps = []
runsbatch5 = {}
runsbatch10 = {}
runsukui = {}
runsscipy = {}
fiterror = {}
diffusions = {}
for temp in multiple:
    count = 0
    temps.append(temp)
    for item in multiple[temp]['all']:
        if runsscipy.get(order[count]) is None:
            runsbatch5[order[count]] = []
            runsbatch10[order[count]] = []
            runsukui[order[count]] = []
            runsscipy[order[count]] = []
            diffusions[order[count]] = []

        runsbatch5[order[count]].append(batch(item, 5))
        runsbatch10[order[count]].append(batch(item, 10))
        runsukui[order[count]].append(ukui(item))
        runsscipy[order[count]].append(st.sem(item))
        diffusions[order[count]].append(sum(item)/len(item))
        print(item)

        count += 1

    count = 0
    for item in multiple[temp]['all_Err']:
        if fiterror.get(order[count]) is None:
            fiterror[order[count]] = []

        fiterror[order[count]].append(sum(item)/len(item))
        count += 1

batch5label = lines.Line2D(
                           [],
                           [],
                           color='b',
                           marker='.',
                           linestyle='None',
                           markersize=8,
                           label='Batch Means (a=5)'
                           )

batch10label = lines.Line2D(
                            [],
                            [],
                            color='r',
                            marker='.',
                            linestyle='None',
                            markersize=8,
                            label='Batch Means (a=10)'
                            )

ukuilabel = lines.Line2D(
                         [],
                         [],
                         color='y',
                         marker='+',
                         linestyle='None',
                         markersize=8,
                         label='Ukui Estimator',
                         markerfacecolor='none'
                         )

scipylabel = lines.Line2D(
                          [],
                          [],
                          color='k',
                          marker='x',
                          linestyle='None',
                          markersize=8,
                          label='Scipy SEM',
                          markerfacecolor='none'
                          )

fitlabel = lines.Line2D(
                        [],
                        [],
                        color='g',
                        marker='^',
                        linestyle='None',
                        markersize=8,
                        label='Fitting Error Averaged',
                        markerfacecolor='none'
                        )

plotlabels = [batch5label, batch10label, ukuilabel, scipylabel, fitlabel]
count = 0
for run in runsscipy:
    fig, ax = pl.subplots(2, figsize=(10, 10))

    ax[0].plot(temps, runsbatch5[run], 'b.')
    ax[0].plot(temps, runsbatch10[run], 'r.')
    ax[0].plot(temps, runsukui[run], 'y+')
    ax[0].plot(temps, runsscipy[run], 'kx')
    ax[0].plot(temps, fiterror[run], 'g^')

    ax[0].set_ylabel('Diffusion Error [*10^-4 cm^2 s^-1]')
    ax[0].legend(handles=plotlabels, loc='best')
    ax[0].grid()

    # Change values to percent error
    runsbatch5percent = [i/j*100.0 for i, j in zip(runsbatch5[run], diffusions[run])]
    runsbatch10percent = [i/j*100.0 for i, j in zip(runsbatch10[run], diffusions[run])]
    runsukuipercent = [i/j*100.0 for i, j in zip(runsukui[run], diffusions[run])]
    runsscipypercent = [i/j*100.0 for i, j in zip(runsscipy[run], diffusions[run])]
    fiterrorpercent = [i/j*100.0 for i, j in zip(fiterror[run], diffusions[run])]

    ax[1].plot(temps, runsbatch5percent, 'b.')
    ax[1].plot(temps, runsbatch10percent, 'r.')
    ax[1].plot(temps, runsukuipercent, 'y+')
    ax[1].plot(temps, runsscipypercent, 'kx')
    ax[1].plot(temps, fiterrorpercent, 'g^')

    ax[1].set_ylabel('Diffusion Percent Error')
    ax[1].set_xlabel('Temperature [K]')
    ax[1].grid()

    ax[0].set_title(run)

    fig.tight_layout()
    fig.savefig('../'+run)

    count += 1

fig, ax, = pl.subplots(2, figsize=(10, 10))
for temp in regular:
    for run in regular[temp]['all']:
        ax[0].plot(temp, run, '.b')

    for run in regular[temp]['all_Err']:
        ax[1].plot(temp, run, '.r')

    ax[0].set_ylabel('Diffusion Error [*10^-4 cm^2 s^-1]')
    ax[0].legend(handles=plotlabels, loc='best')
    ax[0].grid()

    ax[1].set_ylabel('Diffusion Fit Error')
    ax[1].set_xlabel('Temperature [K]')
    ax[1].grid()

fig.tight_layout()
fig.savefig('../singles')
