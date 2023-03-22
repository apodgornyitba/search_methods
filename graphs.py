from cmath import nan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

x = np.array([3, 4, 5, 6, 7, 8, 9, 10, 11])
y = {}

algs = []
cols = []

cost_fig, cost_ax = plt.subplots(figsize=(12, 8))
time_fig, time_ax = plt.subplots(figsize=(12, 8))
frontier_fig, frontier_ax = plt.subplots(figsize=(12, 8))
expanded_fig, expanded_ax = plt.subplots(figsize=(12, 8))  # figsize=(7, 4)

# Read output file
for i in x:
    df = pd.read_csv('./results/output{}.csv'.format(i), keep_default_na=False, na_values=False)
    groupby_alg = df.groupby("Algorithm")
    
    for name_alg, group_alg in groupby_alg:
        groupby_heuristic = group_alg.groupby("Heuristic")
        for name_h, group_h in groupby_heuristic:
            alg_name = name_alg
            if name_h:
                alg_name = alg_name + ', {}'.format(name_h)

            if alg_name not in algs:
                algs.append(alg_name)

            if alg_name not in y:
                y[alg_name] = {}
            
            if alg_name not in y:
                y[alg_name] = {}
            
            if alg_name not in y:
                y[alg_name] = {}
            
            if alg_name not in y:
                y[alg_name] = {}
            
            if alg_name not in y:
                y[alg_name] = {}
            
            if alg_name not in y:
                y[alg_name] = {}
            
            if alg_name not in y:
                y[alg_name] = {}
            
            if alg_name not in y:
                y[alg_name] = {}
            
            for col in group_h:
                if col not in ["Algorithm", "Heuristic"]:
                    if col not in cols:
                        cols.append(col)
                    #print(group[col])
                    if col not in y[alg_name]:
                        y[alg_name][col] = {}
                        y[alg_name][col]['values'] = []
                        y[alg_name][col]['errors'] = []
                    y[alg_name][col]['values'].append(group_h[col].mean())
                    #print('{}->{}->\'values\': {}'.format(alg_name, col, group[col].mean()))
                    y[alg_name][col]['errors'].append(group_h[col].std())
                    #print('{}->{}->\'errors\': {}'.format(alg_name, col, group[col].std()))
                    #if col == 'Cost':
                        #print(y[alg_name][col]['values'][-1])

legends = []
#print(algs)
#print(cols)
for alg in algs:
    legends.append(alg)
    for col in cols:
        #print('{}, {}: {}'.format(alg, col, y[alg][col]))
        match col:
            case 'Cost':
                cost_ax.errorbar(x=x[0:len(y[alg][col]['values'])], y=y[alg][col]['values'], yerr=y[alg][col]['errors'], linestyle='dotted', fmt='o', capsize=6)
            case 'Time elapsed':
                time_ax.errorbar(x=x[0:len(y[alg][col]['values'])], y=y[alg][col]['values'], yerr=y[alg][col]['errors'], linestyle='dotted', fmt='o', capsize=6)
            case 'Frontier Nodes':
                frontier_ax.errorbar(x=x[0:len(y[alg][col]['values'])], y=y[alg][col]['values'], yerr=y[alg][col]['errors'], linestyle='dotted', fmt='o', capsize=6)
            case 'Expanded Nodes':
                expanded_ax.errorbar(x=x[0:len(y[alg][col]['values'])], y=y[alg][col]['values'], yerr=y[alg][col]['errors'], linestyle='dotted', fmt='o', capsize=6)


cost_ax.legend(legends)
time_ax.legend(legends)
frontier_ax.legend(legends)
expanded_ax.legend(legends)

        

#     for name, group in groupbydf:
#         for alg_heuristic in group['Heuristic']:
#             #print(alg_heuristic)
#             #print(alg_heuristic)
#             alg_name = name
#             if alg_heuristic:
#                 alg_name = alg_name + ', {}'.format(alg_heuristic)

#             if alg_name not in algs:
#                 algs.append(algs)

#             if alg_name not in y:
#                 y[alg_name] = {}
            
#             if alg_name not in y:
#                 y[alg_name] = {}
            
#             if alg_name not in y:
#                 y[alg_name] = {}
            
#             if alg_name not in y:
#                 y[alg_name] = {}
            
#             if alg_name not in y:
#                 y[alg_name] = {}
            
#             if alg_name not in y:
#                 y[alg_name] = {}
            
#             if alg_name not in y:
#                 y[alg_name] = {}
            
#             if alg_name not in y:
#                 y[alg_name] = {}
            
#             print()
#             for col in group:
#                 print(group[col])
#                 if col not in ["Algorithm", "Heuristic"]:
#                     if col not in cols:
#                         cols.append(col)
#                     #print(group[col])
#                     if col not in y[alg_name]:
#                         y[alg_name][col] = {}
#                         y[alg_name][col]['values'] = []
#                         y[alg_name][col]['errors'] = []
#                     y[alg_name][col]['values'].append(group[col].mean())
#                     #print('{}->{}->\'values\': {}'.format(alg_name, col, group[col].mean()))
#                     y[alg_name][col]['errors'].append(group[col].std())
#                     #print('{}->{}->\'errors\': {}'.format(alg_name, col, group[col].std()))
#                     #if col == 'Cost':
#                         #print(y[alg_name][col]['values'][-1])

# for alg in alg_name:
#     for col in cols:
#         print(len(y[alg_name][col]['values']))
#         cost_ax.errorbar(x=x[0:len(y[alg_name][col]['values'])], y=y[alg_name][col]['values'], yerr=y[alg_name][col]['errors'], linestyle='dotted', fmt='o', capsize=6)
#         time_ax.errorbar(x=x[0:len(y[alg_name][col]['values'])], y=y[alg_name][col]['values'], yerr=y[alg_name][col]['errors'], linestyle='dotted', fmt='o', capsize=6)
#         frontier_ax.errorbar(x=x[0:len(y[alg_name][col]['values'])], y=y[alg_name][col]['values'], yerr=y[alg_name][col]['errors'], linestyle='dotted', fmt='o', capsize=6)
#         expanded_ax.errorbar(x=x[0:len(y[alg_name][col]['values'])], y=y[alg_name][col]['values'], yerr=y[alg_name][col]['errors'], linestyle='dotted', fmt='o', capsize=6)


cost_ax.set_xlim((3, 11))
cost_ax.set_title('Costo medio de cada algoritmo')
time_ax.set_xlim((3, 11))
time_ax.set_title('Tiempo medio de cada algoritmo')
frontier_ax.set_xlim((3, 11))
frontier_ax.set_title('Cantidad de nodos frontera media de cada algoritmo')
expanded_ax.set_xlim((3, 11))
expanded_ax.set_title('Cantidad de nodos expandidos media de cada algoritmo')

plt.show()


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
