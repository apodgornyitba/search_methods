from cmath import nan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

x = np.array([3, 4, 5, 6, 7, 8, 9])
y = {}

algs = []
cols = []

cost_fig, cost_ax = plt.subplots(figsize=(12, 8))
time_fig, time_ax = plt.subplots(figsize=(12, 8))
frontier_fig, frontier_ax = plt.subplots(figsize=(12, 8))
expanded_fig, expanded_ax = plt.subplots(figsize=(12, 8))

colors = ['red', 'blue', 'yellow', 'green', 'orange', 'purple', 'brown', 'pink']

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
                if col not in ["Algorithm", "Heuristic", "Result"]:
                    if col not in cols:
                        cols.append(col)
                    if col not in y[alg_name]:
                        y[alg_name][col] = {}
                        y[alg_name][col]['values'] = []
                        y[alg_name][col]['errors'] = []
                    y[alg_name][col]['values'].append(group_h[col].mean())
                    y[alg_name][col]['errors'].append(group_h[col].std())

legends = []
color_idx = 0
for alg in algs:
    legends.append(alg)
    for col in cols:
        match col:
            case 'Cost':
                cost_ax.errorbar(x=x[0:len(y[alg][col]['values'])], y=y[alg][col]['values'], yerr=y[alg][col]['errors'], linestyle='dotted', fmt='o', capsize=4, color=colors[color_idx])
            case 'Time elapsed':
                time_ax.errorbar(x=x[0:len(y[alg][col]['values'])], y=y[alg][col]['values'], yerr=y[alg][col]['errors'], linestyle='dotted', fmt='o', capsize=4, color=colors[color_idx])
            case 'Frontier Nodes':
                frontier_ax.errorbar(x=x[0:len(y[alg][col]['values'])], y=y[alg][col]['values'], yerr=y[alg][col]['errors'], linestyle='dotted', fmt='o', capsize=4, color=colors[color_idx])
            case 'Expanded Nodes':
                expanded_ax.errorbar(x=x[0:len(y[alg][col]['values'])], y=y[alg][col]['values'], yerr=y[alg][col]['errors'], linestyle='dotted', fmt='o', capsize=4, color=colors[color_idx])
    color_idx += 1

cost_ax.legend(legends)
time_ax.legend(legends)
frontier_ax.legend(legends)
expanded_ax.legend(legends)

cost_ax.set_xlim((x[0], x[-1]+1))
cost_ax.set_title('Costo medio de cada algoritmo')
cost_ax.set_xlabel('Tamaño del tablero', fontsize=12)
cost_ax.set_ylabel('Cantidad de cambios de color', fontsize=12)
time_ax.set_xlim((x[0], x[-1]+1))
time_ax.set_title('Tiempo medio de cada algoritmo')
time_ax.set_xlabel('Tamaño del tablero', fontsize=12)
time_ax.set_ylabel('Tiempo (s)', fontsize=12)
frontier_ax.set_xlim((x[0], x[-1]+1))
frontier_ax.set_title('Cantidad de nodos frontera media de cada algoritmo')
frontier_ax.set_xlabel('Tamaño del tablero', fontsize=12)
frontier_ax.set_ylabel('Cantidad de nodos', fontsize=12)
expanded_ax.set_xlim((x[0], x[-1]+1))
expanded_ax.set_title('Cantidad de nodos expandidos media de cada algoritmo')
expanded_ax.set_xlabel('Tamaño del tablero', fontsize=12)
expanded_ax.set_ylabel('Cantidad de nodos', fontsize=12)

plt.show()
