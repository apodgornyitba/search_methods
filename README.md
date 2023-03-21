# Fill-Zone solver

**Fill-Zone solver** es un programa que encuentra soluciones para distintos tableros del juego Fill-Zone, mediante los algoritmos de:

- Deep First Search **(DFS)**
- Breadth First Search **(BFS)**
- Greedy Search
- A*

Para los dos últimos hay una serie de heurísticas disponibles para usar, que luego se detallaran en su respectiva sección.

A su vez, se dispone de una interfaz visual creada con la librería [Arcade](https://api.arcade.academy/en/stable/index.html) para observar las soluciones generadas, que igualmente será luego detallada.

## Set up

Primero se deben descargar las dependencias a usar en el programa. Para ello podemos hacer uso de los archivos _Pipfile_ y _Pipfile.lock_ provistos, que ya las tienen detalladas. Para usarlos se debe correr en la carpeta del TP1:

```bash
$> pipenv shell
$> pipenv install
```

Esto creará un nuevo entorno virtual, en el que se instalarán las dependencias a usar, que luego se borrarán una vez se cierre el entorno.

__NOTA:__ Previo a la instalación se debe tener descargado __python__ y __pipenv__, pero se omite dicho paso en esta instalación.

## Uso

### Algoritmo generador de soluciones

El programa encargado de la resolución del juego es ```solver.py```, y tiene dos modos de ejecución:
- A través de una grilla pasada como input:
```shell
# python solver_file input_file max_turns
$> python ./game/solver.py ./input_grids/10x10.txt 30
```
- Usando una grilla aleatoria generada en runtime:
```shell
# python solver_file -r grid_size color_amount max_turns
$> python ./game/solver.py -r 10 6 30
```

Además, el algoritmo genera archivos de salida con la grilla evaluada y la solución encontrada para dicha grilla, dentro de la carpeta ```solutions``` donde, por ejemplo, el archivo __"10x10.txt"__ genera, usando los algoritmos DFS y BFS, los correspondientes archivos de salida __"DFS-sol-10x10.txt"__ y __"BFS-sol-10x10.txt"__

### Visualizador de soluciones

Este programa muestra visualmente cómo sería el juego usando un camino solución generado por el algoritmo, usando de base los archivos de solución ya mencionados.

Así, basta llamar al programa ```game.py``` pasando un archivo solución, de la forma:

```bash
# python visualizer_file solution_file
$> python ./game/game.py ./solutions/DFS-sol-10x10.txt
```