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

## Uso

TODO: Fill