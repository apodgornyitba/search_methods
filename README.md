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

- A través de una grilla pasada como input
- Usando una grilla aleatoria generada en runtime

Ambos modos son configurables mediante el archivo ```config.json``` presente, donde si se provee un __file_path__ como atributo se usará la grilla presente en dicho archivo para la ejecución del programa. Caso contrario se deberán proveer atributos sobre la grilla a generar, que son su __grid_size__ y __color_amount__.

```json
{
    "file_path": "./input_grids/3x3.txt",
    ...
    ó
    ...
    "grid_size": 3,
    "color_amount": 6,
}
```

Luego están los atributos presentes en ambos casos, que son:
- __methods__: Booleans para elegir los algoritmos a correr.
- __turns__: Cantidad máxima de turnos para resolver el juego.
- __heuristic__: Nombre de la heurística a usar para los métodos informados, si se corren. Esta puede ser
    - ```remaining_colors_heuristic```
    - ```bronson_distance_heuristic```
    - ```color_fraction_heuristic``` (no admisible)

De todas formas se proveen dos archivos de ejemplo, ```file_grid_example.json``` y ```random_grid_example.json```, que sirven de ejemplo para los respectivos modos de grilla de input y grilla generada.

### Archivos de salida

El algoritmo genera archivos de salida con la grilla evaluada y la solución encontrada para dicha grilla, dentro de la carpeta ```solutions``` donde, por ejemplo, el archivo __"10x10.txt"__ genera, usando los algoritmos DFS y BFS, los correspondientes archivos de salida __"DFS-sol-10x10.txt"__ y __"BFS-sol-10x10.txt"__.

El formato de dichos archivos es de primero la grilla inicial y luego la serie de acciones necesaria para resolverla, como por ejemplo:

```bash
# Grilla de 4x4 y 4 colores
WHITE GREEN WHITE PURPLE 
RED WHITE RED RED 
PURPLE PURPLE RED PURPLE 
PURPLE WHITE RED GREEN 
RED
PURPLE
RED
PURPLE
WHITE
GREEN
```

También se generan estadísticas sobre cada ejecución en la carpeta ```results``` en formato ```.csv```, donde el archivo en que se encuentre dicho resultado depende del tamaño de la grilla, siendo que una grilla de tamaño __NxN__ tendrá su resultado en el archivo __outputN.csv__. Estas estadísticas pueden ser luego visualizadas corriendo el script __graphs.py__, que genera gráficos sobre
- Costo estimado de solución
- Tiempo de ejecución
- Cantidad de nodos expandidos
- Cantidad de nodos frontera

### Visualizador de soluciones

Este programa muestra visualmente cómo sería el juego usando un camino solución generado por el algoritmo, usando de base los archivos de solución ya mencionados.

Así, basta llamar al programa ```game.py``` pasando un archivo solución, de la forma:

```bash
# python visualizer_file solution_file
$> python ./back/game.py ./solutions/DFS-sol-10x10.txt
```
