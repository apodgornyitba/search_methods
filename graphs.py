import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read output file
df = pd.read_csv('./results/output3.csv')

groupbydf = df.groupby("Algorithm")

y_mean_costs = {}
y_costs_errs = {}

y_times = {}
y_times_errs = {}

y_frontiers = {}
y_frontiers_errs = {}

y_expandeds = {}
y_expandeds_errs = {}

fig, ax = plt.subplots(figsize=(7, 4))
x = np.array([3])

for name, group in groupbydf:
    alg_name = name
    if group['Heuristic'] is not None:
        alg_name = alg_name + ', {}'.format(group['Heuristic'])
    for col in group:
        if col not in ["Algorithm", "Heuristic"]:
            print(group[col])
            y_mean_costs[alg_name] = group[col].mean()
            y_costs_errs[alg_name] = group[col].std()
    ax.errorbar(x=x, y=y_costs_errs[alg_name], yerr=y_costs_errs[alg_name], linestyle='dotted', fmt='o', capsize=6)
    #print(y_mean_costs)


# lower & upper limits of the error



# standard error bars


# including upper limits
#ax.errorbar(x, y + 0.5, yerr=yerr, uplims=uplims,
            #linestyle=ls)

# including lower limits
#ax.errorbar(x, y + 1.0, yerr=yerr, lolims=lolims,
            #linestyle=ls)

# including upper and lower limits
#ax.errorbar(x, y + 1.5, yerr=yerr,
            #lolims=lolims, uplims=uplims,
            #marker='o', markersize=8,
            #linestyle=ls)

# Plot a series with lower and upper limits in both x & y
# constant x-error with varying y-error

# do the plotting
#ax.errorbar(x, y + 2.1, yerr=yerr,
#            xlolims=xlolims, xuplims=xuplims,
#            uplims=uplims, lolims=lolims,
#            marker='o', markersize=8,
#            linestyle='none')

# tidy up the figure
ax.set_xlim((0, 5.5))
ax.set_title('Errorbar upper and lower limits')
plt.show()